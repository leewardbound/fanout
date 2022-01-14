import graphene
from graphene_validator.decorators import validated
from graphene_validator.errors import ValidationError

from fanout.apps.federation.schema.queries import Activity


@validated
class CreateNoteInput(graphene.InputObjectType):
    actorId = graphene.String(required=True)
    content = graphene.String(required=True)

    @staticmethod
    def validate_content(content, info, **input):
        content = content.strip()
        if not content:
            raise ValidationError("Content cant be blank")
        return content


class CreateNote(graphene.Mutation):
    class Arguments:
        input = CreateNoteInput()

    activity = graphene.Field(Activity)

    @classmethod
    def mutate(cls, root, info, input):
        from fanout.apps.federation.models import Activity, ActivityTypes, Actor

        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not Authenticated")
        actor = Actor.objects.get(pk=input["actorId"])
        note = actor.note_set.create(content=input["content"])
        activity = Activity.objects.create(actor=actor, object=note, type=ActivityTypes.CREATE)

        return CreateNote(activity=activity)


class Mutations(object):
    createNote = CreateNote.Field()
