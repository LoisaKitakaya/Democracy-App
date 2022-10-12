import graphene
from graphene_django import DjangoObjectType
from users.models import User

# my object type

class UserType(DjangoObjectType):

    class Meta:

        model = User

        exclude = ('password',)

# GraphQL Queries

class Query(graphene.ObjectType):
    
    # queries

    all_users = graphene.List(UserType)

    # resolving queries

    def resolve_all_users(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return User.objects.all()

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    pass