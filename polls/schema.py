import graphene
from graphene_django import DjangoObjectType
from organizers.models import Workspace, Organizer
from polls.models import Poll, Candidate

# my object type

class PollType(DjangoObjectType):

    class Meta:

        model = Poll

        fields = '__all__'

# my object type

class CandidateType(DjangoObjectType):

    class Meta:

        model = Candidate

        fields = '__all__'

# GraphQL Queries

class Query(graphene.ObjectType):
    
    # queries

    all_polls = graphene.List(PollType)
    all_candidates = graphene.List(CandidateType)

    # resolving queries

    def resolve_all_polls(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        organizer = Organizer.objects.get(user=user)

        return Poll.objects.filter(organizer=organizer)

    def resolve_all_candidates(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return Workspace.objects.all()

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    pass