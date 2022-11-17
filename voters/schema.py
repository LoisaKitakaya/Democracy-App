import graphene
from graphene_django import DjangoObjectType
from voters.models import Voter
from organizers.models import Workspace, Organizer
from users.models import User
from django.contrib.auth.models import Permission
from app.accounts import VoterAction
from graphql_jwt.decorators import permission_required

# my object type

class VoterType(DjangoObjectType):

    class Meta:

        model = Voter

        fields = '__all__'

# GraphQL Queries

class Query(graphene.ObjectType):
    
    # queries

    my_voter_account = graphene.Field(VoterType)

    # resolving queries

    @permission_required("ballot.add_ballot")
    def resolve_my_voter_account(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return Voter.objects.get(user=user)

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

        try:

            is_organizer = Organizer.objects.get(user=user)

        except:

            print("User is not associated with voter account")

        else:

            if is_organizer:

                raise Exception("You cannot register as a voter. You already have an organizer account")

        selected_workspace = Workspace.objects.get(name=workspace)

        voter_object = VoterAction(
            user=user,
            workspace=selected_workspace
        )

        voter = voter_object.register_voter_to_workspace(country=country)

        try:

            organizer_permissions = Permission.objects.get(name="Can add ballot")

        except Permission.DoesNotExist:

            print("Permission does not exist")

        else:

            user.user_permissions.add(organizer_permissions)

        return CreateVoter(voter=voter)

class UpdateVoter(graphene.Mutation):

    class Arguments:

        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        country = graphene.String(required=True)

    voter = graphene.Field(VoterType)

    @classmethod
    def mutate(
        cls, root, info,
        username,
        first_name,
        last_name,
        country
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        try:

            User.objects.get(username=username)

        except:

            print("This username is available")

        else:

            raise Exception("The username provided has already been used")

        try:

            update_user = User.objects.get(id=int(user.id))

            print(update_user)
            
        except:

            print("This user account does not exist")

        else:

            update_user.username = username
            update_user.first_name = first_name
            update_user.last_name = last_name

            update_user.save()

        try:

            voter = Voter.objects.get(user=user)

        except:

            print("Account does not exist")

            raise Exception("This account does not exist")

        else:

            voter.country = country

            voter.save()

        return UpdateVoter(voter=voter)

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    register_voter = CreateVoter.Field()
    update_voter = UpdateVoter.Field()