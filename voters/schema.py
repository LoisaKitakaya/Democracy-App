import graphene
from graphene_django import DjangoObjectType
from voters.models import Voter

# my object type

class VoterType(DjangoObjectType):

    class Meta:

        model = Voter

        fields = '__all__'

# GraphQL Queries

class Query(graphene.ObjectType):
    
    # queries

    all_voters = graphene.List(VoterType)

    # resolving queries

    def resolve_all_voters(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return Voter.objects.all()

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    pass