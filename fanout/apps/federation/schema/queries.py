import graphene
from graphene_django import DjangoObjectType
from fanout.apps.federation import models
from fanout.apps.content import models as contentModels

class Note(DjangoObjectType):
    class Meta:
        model = contentModels.Note

class Activity(DjangoObjectType):
    objectType = graphene.String()
    note = graphene.Field(Note)

    def resolve_objectType(root, info):
        return root.object._meta.model_name

    def resolve_note(root, info):
        if isinstance(root.object, contentModels.Note):
            return root.object

    class Meta:
        model = models.Activity

class Queries(graphene.ObjectType):
    activities = graphene.List(Activity, actorId=graphene.ID(required=True))

    def resolve_activities(self, info, actorId):
        return models.Activity.objects.filter(actor_id=actorId).prefetch_related(
            'object'
        )
