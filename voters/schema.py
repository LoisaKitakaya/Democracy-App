import graphene
from graphene_django import DjangoObjectType
from voters.models import Voter
from organizers.models import Workspace, Organizer

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

# voter model mutations

class CreateVoter(graphene.Mutation):

    class Arguments:

        country = graphene.String(required=True)
        workspace = graphene.String(required=True)

    voter = graphene.Field(VoterType)

    @classmethod
    def mutate(
        cls, root, info,
        country,
        workspace
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        is_organizer = Organizer.objects.get(user=user)

        if is_organizer:

            raise Exception("You cannot register as a voter. You already have an organizer account")

        selected_workspace = Workspace.objects.get(name=workspace)

        voter = Voter.objects.create(
            user=user,
            country=country,
            workspace=selected_workspace
        )

        return CreateVoter(voter=voter)

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    register_voter = CreateVoter.Field()