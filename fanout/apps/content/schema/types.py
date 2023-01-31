from graphene_django import DjangoObjectType

from fanout.apps.content import models


class Note(DjangoObjectType):
    class Meta:
        model = models.Note


class Image(DjangoObjectType):
    class Meta:
        model = models.Image
