import graphene

import fanout.apps.content.schema.mutations
import fanout.apps.customers.schema.mutations
import fanout.apps.federation.schema.queries
import fanout.apps.users.schema


class Query(
    fanout.apps.users.schema.Queries,
    fanout.apps.federation.schema.queries.Queries,
    graphene.ObjectType,
):
    pass


class Mutation(
    fanout.apps.users.schema.Mutations,
    fanout.apps.customers.schema.mutations.Mutations,
    fanout.apps.content.schema.mutations.Mutations,
    graphene.ObjectType,
):
    pass


application_schema = graphene.Schema(query=Query, mutation=Mutation)
