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

class CandidateResults(graphene.ObjectType):

    name = graphene.String()
    image = graphene.String()
    total_votes = graphene.Int()

# GraphQL Queries

class Query(graphene.ObjectType):
    
    # queries

    results = graphene.List(CandidateResults, poll_id=graphene.String(required=True))

    # resolving queries

    def resolve_results(root, info, poll_id):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        try:

            poll = Poll.objects.get(id=int(poll_id))

        except:

            print("Poll does not exist")

            raise Exception("This poll does not exist")

        try:

            candidates_in_poll = Candidate.objects.filter(poll=poll)

        except:

            print("This poll has no registered candidates")

        poll_results = []

        candidate_count = []

        for candidate in candidates_in_poll:

            try:

                image = candidate.image.url

            except:

                print("Candidate does not have an existing avatar")

                image = "https://via.placeholder.com/300"

            result = {
                'candidate': f'{candidate.first_name} {candidate.last_name}',
                'image': f'{image}',
                'total': len(Ballot.objects.filter(candidate=candidate)),
            }

            candidate_count.append(result)

        for x in range(len(candidate_count)):

            candidate_results = CandidateResults(
                name=candidate_count[x]["candidate"],
                image=candidate_count[x]["image"],
                total_votes=int(candidate_count[x]["total"])
            )

            poll_results.append(candidate_results)

        return poll_results

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

                raise Exception("You have already voted on this poll. You cannot vote more than once!")

        ballot = Ballot.objects.create(
            poll=cast_poll,
            candidate=selected_candidate,
            voter=voter
        )

        return CastBallot(ballot=ballot)

class Mutation(graphene.ObjectType):

    cast_vote = CastBallot.Field()