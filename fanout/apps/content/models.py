from django.db import models

from fanout.apps.federation.models import ActivityPubObjectMixin
from fanout.apps.utils.models import TimestampMixin

class ObjectTypes(models.TextChoices):
    APPLICATION = "Application"
    ARTICLE = "Article"
    AUDIO = "Audio"
    COLLECTION = "Collection"
    DOCUMENT = "Document"
    EVENT = "Event"
    GROUP = "Group"
    IMAGE = "Image"
    NOTE = "Note"
    OBJECT = "Object"
    ORDERED_COLLECTION = "OrderedCollection"
    ORGANIZATION = "Organization"
    PAGE = "Page"
    PERSON = "Person"
    PLACE = "Place"
    PROFILE = "Profile"
    RELATIONSHIP = "Relationship"
    SERVICE = "Service"
    TOMBSTONE = "Tombstone"
    VIDEO = "Video"


class ContentBase(ActivityPubObjectMixin, TimestampMixin):
    actor = models.ForeignKey('federation.Actor', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class FileContentBase(ContentBase):
    content_url = models.CharField(max_length=2048)

    class Meta:
        abstract = True


class Note(ContentBase):
    content = models.TextField(max_length=50_000)
