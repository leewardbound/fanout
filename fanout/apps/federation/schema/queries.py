import graphene

from fanout.apps.federation.schema.types import Activity


class Queries(graphene.ObjectType):
    activities = graphene.List(Activity, actorId=graphene.ID(required=True))

    def resolve_activities(self, info, actorId):
        from fanout.apps.federation import models

        return models.Activity.objects.filter(actor_id=actorId).prefetch_related("object")
