import graphene
from graphene_django import DjangoObjectType
from polls.models import Poll, Candidate
from ballot.models import Ballot
from voters.models import Voter
from graphql_jwt.decorators import permission_required

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

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return Ballot.objects.all()

# GraphQL Mutations

class CastBallot(graphene.Mutation):

    class Arguments:

        poll_id = graphene.String(required=True)
        candidate_id = graphene.String(required=True)

    ballot = graphene.Field(BallotType)

    @classmethod
    @permission_required("ballot.add_ballot")
    def mutate(
        cls, root, info,
        poll_id,
        candidate_id
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        try:

            cast_poll = Poll.objects.get(id=int(poll_id))
            
        except:

            print("This poll does not exist")

            raise Exception("This poll does not exist")

        try:

            selected_candidate =Candidate.objects.get(id=int(candidate_id))

        except:

            print("This candidate does not exist")

            raise Exception("This candidate does not exist")

        try:

            voter = Voter.objects.get(user=user)

        except:

            print("This voter does not exist")

            raise Exception("This voter does not exist")

        try:

            has_voted = Ballot.objects.filter(poll=cast_poll, voter=voter)

        except:

            print("Voter has not voted on this poll")

        else:

            if has_voted:

                raise Exception("You have already voted on this poll. You cannot vote twice!")

        ballot = Ballot.objects.create(
            poll=cast_poll,
            candidate=selected_candidate,
            voter=voter
        )

        return CastBallot(ballot=ballot)

class Mutation(graphene.ObjectType):

    cast_vote = CastBallot.Field()