import graphene
from graphene_django import DjangoObjectType

from fanout.apps.customers import models


class CustomerDataPoint(graphene.ObjectType):
    key = graphene.String()
    value = graphene.String()


class Customer(DjangoObjectType):
    datapoints = graphene.List(CustomerDataPoint)

    class Meta:
        model = models.Customer
