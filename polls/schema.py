import graphene
from graphene_django import DjangoObjectType
from organizers.models import Workspace, Organizer
from polls.models import Poll, Candidate
from graphql_jwt.decorators import permission_required

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

    organizer_polls = graphene.List(PollType)
    organizer_candidates = graphene.List(CandidateType)

    # resolving queries

    def resolve_organizer_polls(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        organizer = Organizer.objects.get(user=user)

        return Poll.objects.filter(organizer=organizer)

    def resolve_organizer_candidates(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return Workspace.objects.all()

# Poll model mutations

class CreatePoll(graphene.Mutation):

    class Arguments:

        seat = graphene.String(required=True)
        intro = graphene.String(required=True)
        begin_date = graphene.Date(required=True)
        end_date = graphene.Date(required=True)

    poll = graphene.Field(PollType)

    @classmethod
    @permission_required("polls.add_poll")
    def mutate(
        cls, root, info,
        seat,
        intro,
        begin_date,
        end_date
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        organizer = Organizer.objects.get(user=user)

        workspace = Workspace.objects.get(organizer=organizer)

        poll = Poll.objects.create(
            seat=seat,
            intro=intro,
            begin_date=begin_date,
            end_date=end_date,
            organizer=organizer,
            workspace=workspace
        )

        return CreatePoll(poll=poll)

class EditPoll(graphene.Mutation):

    class Arguments:

        id = graphene.Int(required=True)
        seat = graphene.String(required=True)
        intro = graphene.String(required=True)
        begin_date = graphene.Date(required=True)
        end_date = graphene.Date(required=True)

    poll = graphene.Field(PollType)

    @classmethod
    @permission_required("polls.add_poll")
    def mutate(
        cls, root, info,
        id,
        seat,
        intro,
        begin_date,
        end_date
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        poll = Poll.objects.get(id=id)

        poll.seat = seat,
        poll.intro = intro
        poll.begin_date=begin_date
        poll.end_date = end_date
        
        poll.save()

        return CreatePoll(poll=poll)

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    create_poll = CreatePoll.Field()
    update_poll = EditPoll.Field()