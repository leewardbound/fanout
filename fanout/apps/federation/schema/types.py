import graphene
from graphene_django import DjangoObjectType

from fanout.apps.content.schema.types import Image, Note
from fanout.apps.federation import models


class Activity(DjangoObjectType):
    objectType = graphene.String()
    note = graphene.Field(Note)
    image = graphene.Field(Image)

    def resolve_objectType(root, info):
        return root.object._meta.model_name

    def resolve_note(root, info):
        from fanout.apps.content.models import Note

        if isinstance(root.object, Note):
            return root.object

    def resolve_image(root, info):
        from fanout.apps.content.models import Image

        if isinstance(root.object, Image):
            return root.object

    class Meta:
        model = models.Activity
