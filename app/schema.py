import graphene
import graphql_jwt
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

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)