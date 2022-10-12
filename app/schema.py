import graphene
import ballot.schema as ballot
import organizers.schema as organizers
import polls.schema as polls
import users.schema as users
import voters.schema as voters

# GraphQL Queries

class Query(
    # custom queries

    ballot.Query,
    organizers.Query,
    polls.Query,
    users.Query,
    voters.Query,

    # graphene object tpe

    graphene.ObjectType
):
    
    pass

# GraphQL Mutations

class Mutation(
     # custom queries

    ballot.Mutation,
    organizers.Mutation,
    polls.Mutation,
    users.Mutation,
    voters.Mutation,

     # graphene object tpe
    
    graphene.ObjectType
):

    pass

schema = graphene.Schema(query=Query)