from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
# Federated object data includes records created by other services
# which might have a remote URL
from django.utils import timezone

from fanout.apps.federation import keys
from fanout.apps.federation.utils import slugify_username
from fanout.constants import URLPrefixes
from fanout.utils.models import TimestampMixin, from_choices, uuid4_string


def activitypub_id_generator(url_prefix, default_domain=None):
    def _generator(identifier=None, domain=None):
        if default_domain and not domain:
            domain = default_domain
        elif not domain:
            domain = settings.APP_HOSTNAME

        return f"https://{domain}/{url_prefix}/{identifier or uuid4_string()}".lower()

    return _generator


def actor_id_generator(identifier=None, domain=None):
    return activitypub_id_generator(URLPrefixes.ACTORS)(identifier, domain)


class ActivityPubObjectMixin(models.Model):
    id = models.CharField(primary_key=True, max_length=512, default=uuid4_string)

    class Meta:
        abstract = True

    @property
    def is_local(self):
        from .utils import is_local

        return is_local(self.id)


# Remote domains
class Domain(TimestampMixin):
    id = models.CharField(primary_key=True, max_length=512, default=uuid4_string)
    name = models.CharField(unique=True, max_length=255)
    info = models.JSONField(max_length=50000, null=True, blank=True)
    info_updated = models.DateTimeField(null=True, blank=True)
    service_actor = models.ForeignKey(
        "federation.Actor", related_name="managed_domains", on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def is_local(self):
        return self.name == settings.APP_HOSTNAME

    @classmethod
    def LOCAL(cls):
        domain, new = cls.objects.get_or_create(name=settings.APP_HOSTNAME)
        if new:
            domain.service_actor = Actor.objects.create(
                type=ActorTypes.SERVICE,
                display_name="Local System",
                username="system",
                domain=domain,
            )
            domain.save()
        return domain


class ActorTypes(models.TextChoices):
    PERSON = "Person"
    GROUP = "Group"
    ORGANIZATION = "Organization", "Organization or Company"
    APPLICATION = "Application"
    SERVICE = "Service"


class Actor(ActivityPubObjectMixin, TimestampMixin):
    id = models.CharField(primary_key=True, max_length=512, default=actor_id_generator)
    type = models.CharField(max_length=128)
    display_name = models.CharField(max_length=512, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="actors")
    public_key = models.TextField(max_length=5_000, null=True, blank=True)
    private_key = models.TextField(max_length=5_000, null=True, blank=True)
    summary = models.CharField(max_length=512, null=True, blank=True)
    summary_updated = models.DateTimeField(default=timezone.now)
    manually_approves_followers = models.BooleanField(default=False)
    followers_url = models.CharField(max_length=2048, null=True, blank=True)
    inbox_url = models.CharField(max_length=2048, null=True, blank=True)
    outbox_url = models.CharField(max_length=2048, null=True, blank=True)
    profile_url = models.CharField(max_length=2048, null=True, blank=True)
    icon_url = models.CharField(max_length=2048, null=True, blank=True)

    owner = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, related_name="owned_actors", null=True, blank=True
    )

    @property
    def private_key_id(self):
        return "{}#main-key".format(self.id)

    def __str__(self):
        return "{}@{}".format(self.username, self.domain.name)


def build_actor_data(username, **kwargs):
    slugified_username = slugify_username(username)
    domain = kwargs.get("domain")

    private, public = keys.get_key_pair()

    if not domain:
        domain = settings.APP_HOSTNAME

    _type = kwargs.get("type", ActorTypes.PERSON)

    return {
        "username": slugified_username,
        "domain": domain,
        "type": _type,
        "display_name": kwargs.get("name", username),
        "summary": kwargs.get("summary"),
        "manually_approves_followers": False,
        "private_key": private.decode("utf-8"),
        "public_key": public.decode("utf-8"),
        "id": actor_id_generator(slugified_username, domain=domain),
    }


# A subset of Activity Verbs from
# https://github.com/activitystreams/activity-schema/blob/master/activity-schema.md
# This abridged list is for python typing convenience, it is never used to restrict
# activities you might choose to create in your application
class ActivityVerbs(models.TextChoices):
    ACCEPT = "Accept"
    ADD = "Add"
    ANNOUNCE = "Announce"
    ARRIVE = "Arrive"
    BLOCK = "Block"
    CREATE = "Create"
    DELETE = "Delete"
    DISLIKE = "Dislike"
    FLAG = "Flag"
    FOLLOW = "Follow"
    IGNORE = "Ignore"
    INVITE = "Invite"
    JOIN = "Join"
    LEAVE = "Leave"
    LIKE = "Like"
    LISTEN = "Listen"
    MOVE = "Move"
    OFFER = "Offer"
    QUESTION = "Question"
    REJECT = "Reject"
    READ = "Read"
    REMOVE = "Remove"
    SHARE = "Share"
    TENTATIVE_REJECT = "TentativeReject"
    TENTATIVE_ACCEPT = "TentativeAccept"
    TRAVEL = "Travel"
    UNDO = "Undo"
    UPDATE = "Update"
    VIEW = "View"


class InboxItem(models.Model):
    """
    Store activities binding to local actors, with read/unread status.
    """

    actor = models.ForeignKey(Actor, related_name="inbox_items", on_delete=models.CASCADE)
    activity = models.ForeignKey("Activity", related_name="inbox_items", on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[("to", "to"), ("cc", "cc")])
    is_read = models.BooleanField(default=False)


# An Activity
class Activity(ActivityPubObjectMixin, TimestampMixin):
    actor = models.ForeignKey(Actor, related_name="outbox_activities", on_delete=models.CASCADE)
    verb = models.CharField(**from_choices(ActivityVerbs, max_length=32))
    recipients = models.ManyToManyField(Actor, related_name="inbox_activities", through=InboxItem)
    payload = models.JSONField(null=True, blank=True)

    # generic relations
    object_id = models.CharField(max_length=256, null=True, blank=True)
    object_content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="objecting_activities",
    )
    object = GenericForeignKey("object_content_type", "object_id")
    target_id = models.CharField(max_length=256, null=True, blank=True)
    target_content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="targeting_activities",
    )
    target = GenericForeignKey("target_content_type", "target_id")
    related_object_id = models.CharField(max_length=256, null=True, blank=True)
    related_object_content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="related_objecting_activities",
    )
    related_object = GenericForeignKey("related_object_content_type", "related_object_id")
