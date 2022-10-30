import graphene
from graphene_django import DjangoObjectType
from organizers.models import Organizer, Workspace
from voters.models import Voter
from users.models import User
from django.contrib.auth.models import Permission
from graphql_jwt.decorators import permission_required

# my object type

class OrganizerType(DjangoObjectType):

    class Meta:

        model = Organizer

        fields = '__all__'

# my object type

class WorkspaceType(DjangoObjectType):

    class Meta:

        model = Workspace

        fields = '__all__'

# GraphQL Queries

class Query(graphene.ObjectType):
    
    # queries

    organizer_avatar = graphene.String()
    my_organizer_account = graphene.Field(OrganizerType)
    all_workspaces = graphene.List(WorkspaceType)

    # resolving queries

    def resolve_organizer_avatar(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        organizer = Organizer.objects.get(user=user)

        try:

            organizer.image.url

        except:

            print("User has not uploaded an image")

            return "https://via.placeholder.com/300"

        else:

            organizer_avatar = organizer.image.url

            return organizer_avatar

    @permission_required("polls.add_poll")
    def resolve_my_organizer_account(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return Organizer.objects.get(user=user)

    def resolve_all_workspaces(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return Workspace.objects.all()

# Organizer model mutations

class CreateOrganizer(graphene.Mutation):

    class Arguments:

        phone = graphene.String(required=True)
        country = graphene.String(required=True)
        workspace = graphene.String(required=True)

    organizer = graphene.Field(OrganizerType)

    @classmethod
    def mutate(
        cls, root, info,
        phone,
        country,
        workspace
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        try:

            Voter.objects.get(user=user)

        except:

            print("User is not associated with voter account")

        else:

            is_voter = Voter.objects.get(user=user)

            if is_voter:

                raise Exception("You cannot register as an organizer. You already have a voters account")

        try:

            find_workspace = Workspace.objects.get(name=workspace)

        except:

            print("Workspace with provided name does not exist")

        else:

            find_workspace = Workspace.objects.get(name=workspace)

            if find_workspace:

                raise Exception("A workspace with the same name already exists")

        organizer = Organizer.objects.create(
            user=user,
            phone=phone,
            country=country
        )

        Workspace.objects.create(
            organizer=organizer,
            name=workspace
        )

        try:

            organizer_permissions = Permission.objects.get(name="Can add poll")

        except Permission.DoesNotExist:

            print("Permission does not exist")

        else:

            user.user_permissions.add(organizer_permissions)

        return CreateOrganizer(organizer=organizer)

class UpdateOrganizer(graphene.Mutation):

    class Arguments:

        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        phone = graphene.String(required=True)
        country = graphene.String(required=True)
        workspace = graphene.String(required=True)

    organizer = graphene.Field(OrganizerType)

    @classmethod
    def mutate(
        cls, root, info,
        username,
        first_name,
        last_name,
        phone,
        country,
        workspace
    ):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        username_exists = User.objects.get(username=username)

        if username_exists:

            raise Exception("The username provided has already been used")

        else:

            User.objects.filter(id=user.id).update(
                username=username,
                first_name=first_name,
                last_name=last_name
            )

        try:

            organizer = Organizer.objects.get(user=user)

        except:

            print("Account does not exist")

            raise Exception("This account does not exist")

        else:

            organizer.phone = phone
            organizer.country = country

            organizer.save()

        try:

            organizer_workspace = Workspace.objects.get(organizer=organizer)

        except:

            print("Workspace does not exist")

            raise Exception("Workspace does not exist")

        else:

            organizer_workspace.name = workspace

            organizer_workspace.save()

        return UpdateOrganizer(organizer=organizer)

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    register_organizer = CreateOrganizer.Field()
    update_organizer = UpdateOrganizer.Field()