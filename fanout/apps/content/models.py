from django.db import models

from fanout.apps.federation.models import ActivityPubObjectMixin, ActorTypes
from fanout.apps.utils.models import TimestampMixin


class BaseTypes(models.TextChoices):
    OBJECT = "Object"
    COLLECTION = "Collection"
    ORDERED_COLLECTION = "OrderedCollection"


class ObjectTypes(models.TextChoices):
    # Actor Types
    PERSON = "Person"
    GROUP = "Group"
    ORGANIZATION = "Organization", "Organization or Company"
    APPLICATION = "Application"
    SERVICE = "Service"

    # Content Types
    ARTICLE = "Article"
    AUDIO = "Audio"
    DOCUMENT = "Document"
    EVENT = "Event"
    IMAGE = "Image"
    NOTE = "Note"
    PAGE = "Page"
    PLACE = "Place"
    PROFILE = "Profile"
    RELATIONSHIP = "Relationship"
    TOMBSTONE = "Tombstone"
    VIDEO = "Video"


class ContentBase(ActivityPubObjectMixin, TimestampMixin):
    actor = models.ForeignKey("federation.Actor", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class FileContentBase(ContentBase):
    content_url = models.CharField(max_length=2048)

    class Meta:
        abstract = True


class Note(ContentBase):
    type = ObjectTypes.NOTE
    content = models.TextField(max_length=50_000)


class Image(FileContentBase):
    type = ObjectTypes.IMAGE
