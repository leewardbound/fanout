from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from fanout.apps.federation.models import build_actor_data
from fanout.utils.models import TimestampMixin, UUIDMixin


def get_library_path(instance, fn):
    owner_id = instance.library.id
    return f"media/{owner_id}/{fn}"


class User(TimestampMixin, UUIDMixin, AbstractUser):
    pass


class MediaLibrary(TimestampMixin, UUIDMixin):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class MediaLibraryFile(TimestampMixin, UUIDMixin):
    library = models.ForeignKey(MediaLibrary, on_delete=models.CASCADE)
    path = models.CharField(max_length=1024)
    file = models.FileField("File", upload_to=get_library_path, null=True, blank=True)


class AuditLogType(models.TextChoices):
    SUBSCRIPTION_CREATED = "subscription.created", "Subscription Created"
    SUBSCRIPTION_UPDATED = "subscription.updated", "Subscription Updated"
    CUSTOMER_CREATED = "customer.created", "Customer Created"
    CUSTOMER_UPDATED = "customer.updated", "Customer Updated"


class AuditLog(TimestampMixin, UUIDMixin):
    performing_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="audit_log")
    type = models.CharField(max_length=64, db_index=True)
    message = models.CharField(max_length=512, null=True, blank=True)

    succeeded = models.BooleanField(default=True)
    extra_data = models.JSONField(null=True, blank=True)

    target_id = models.UUIDField(null=True, blank=True)
    target_content_type = models.ForeignKey(
        ContentType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="targeting_audit_logs",
    )
    target = GenericForeignKey("target_content_type", "target_id")


def create_actor_for_user(user, **kwargs):
    args = build_actor_data(user.username)
    args.update(kwargs)

    from fanout.apps.federation.models import Actor

    return Actor.objects.create(user=user, **args)
