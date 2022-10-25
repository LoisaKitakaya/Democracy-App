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
    candidate_avatar = graphene.String(id=graphene.String())

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

        organizer = Organizer.objects.get(user=user)

        return Candidate.objects.filter(organizer=organizer)

    def resolve_candidate_avatar(root, info, id):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        candidate = Candidate.objects.get(id=int(id))

        try:

            candidate.image.url

        except:

            print("Candidate does not have an avatar")

            return "https://via.placeholder.com/720x468"

        else:

            candidate_avatar = candidate.image.url

            return candidate_avatar

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

        id = graphene.String(required=True)
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

        poll = Poll.objects.get(id=int(id))

        poll.seat = seat
        poll.intro = intro
        poll.begin_date=begin_date
        poll.end_date = end_date
        
        poll.save()

        return EditPoll(poll=poll)

class RegisterCandidate(graphene.Mutation):

    class Arguments:

        id = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        country = graphene.String(required=True)
        bio = graphene.String(required=True)

    candidate = graphene.Field(CandidateType)

    @classmethod
    @permission_required("polls.add_poll")
    def mutate(
        cls, root, info,
        id,
        first_name,
        last_name,
        email,
        country,
        bio
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        try:

            poll = Poll.objects.get(id=int(id))

        except:

            print("Selected poll does not exist")

            raise Exception("Selected poll does not exist")

        try:

            organizer = Organizer.objects.get(user=user)

        except:

            print("This account does not exist")

            raise Exception("This account does not exist")

        candidate = Candidate.objects.create(
            organizer=organizer,
            poll=poll,
            first_name=first_name,
            last_name=last_name,
            email=email,
            country=country,
            bio=bio
        )

        return RegisterCandidate(candidate=candidate)

class ClosePoll(graphene.Mutation):

    class Arguments:

        id = graphene.String(required=True)

    confirmation = graphene.String()

    @classmethod
    @permission_required("polls.add_poll")
    def mutate(
        cls, root, info,
        id
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        poll = Poll.objects.get(id=int(id))

        poll.open = False

        poll.save()

        confirmation = "This poll has been closed"

        return ClosePoll(confirmation=confirmation)

class DeletePoll(graphene.Mutation):

    class Arguments:

        id = graphene.String(required=True)

    confirmation = graphene.String()

    @classmethod
    @permission_required("polls.add_poll")
    def mutate(
        cls, root, info,
        id
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        poll = Poll.objects.get(id=int(id))

        poll.open = False

        poll.delete()

        confirmation = "This poll has been deleted"

        return DeletePoll(confirmation=confirmation)

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    create_poll = CreatePoll.Field()
    update_poll = EditPoll.Field()
    close_poll = ClosePoll.Field()
    delete_poll = DeletePoll.Field()
    register_candidate = RegisterCandidate.Field()