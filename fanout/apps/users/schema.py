import graphene
from graphene_django import DjangoObjectType

from . import models


class User(DjangoObjectType):
    class Meta:
        model = models.User


class Queries(object):
    users = graphene.List(User)

    def resolve_users(self, info):
        return models.User.objects.all()
