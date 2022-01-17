import re

import graphene
from graphene_validator.decorators import validated
from graphene_validator.errors import InvalidEmailFormat

from fanout.apps.customers import models
from fanout.apps.customers.schema.queries import CustomerDataPoint
from fanout.apps.utils.models import get_client_ip


class CustomerDataPointInput(graphene.InputObjectType):
    key = graphene.String(required=True)
    value = graphene.String(required=True)


class SubscribeByEmailInput(graphene.InputObjectType):
    actorId = graphene.String(required=True)
    email = graphene.String(required=True)
    datapoints = graphene.List(CustomerDataPointInput)

    @staticmethod
    def validate_email(email, info, **input):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not re.fullmatch(regex, email):
            raise InvalidEmailFormat
        return email.strip()


@validated
class SubscribeByEmail(graphene.Mutation):
    class Arguments:
        input = SubscribeByEmailInput()

    email = graphene.String()
    datapoints = graphene.List(CustomerDataPoint)
    created = graphene.Boolean()

    def mutate(self, info, input):
        user = info.context.user
        if user.is_anonymous:
            user = None
        datapoints = {dp["key"]: dp["value"] for dp in input["datapoints"]}
        ip = get_client_ip(info.context.META)
        c = models.Customer.collect_customer(input["email"], user=user, ip=ip, datapoints=datapoints)
        subscription, created = c.subscribe_to_actor(input["actorId"])

        return SubscribeByEmail(
            email=input["email"], datapoints=[{"key": k, "value": v} for k, v in datapoints.items()], created=created
        )


class Mutations(graphene.ObjectType):
    subscribeByEmail = SubscribeByEmail.Field()
