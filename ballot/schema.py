import graphene
from graphene_django import DjangoObjectType
from ballot.models import Ballot

# my object type

class BallotType(DjangoObjectType):

    class Meta:

        model = Ballot

        fields = '__all__'

# GraphQL Queries

class Query(graphene.ObjectType):
    
    # queries

    all_ballots = graphene.List(BallotType)

    # resolving queries

    def resolve_all_ballots(root, info):

        return Ballot.objects.all()

# GraphQL Mutations

class Mutation(graphene.ObjectType):

    pass