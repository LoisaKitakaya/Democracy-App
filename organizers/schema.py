import graphene
from graphene_django import DjangoObjectType
from organizers.models import Organizer, Workspace
from voters.models import Voter

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

    all_organizers = graphene.List(OrganizerType)
    all_workspaces = graphene.List(WorkspaceType)

    # resolving queries

    def resolve_all_organizers(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return Organizer.objects.all()

    def resolve_all_workspaces(root, info):

        user = info.context.user

        if not user.is_authenticated:
            
            raise Exception("Authentication credentials were not provided")

        return Workspace.objects.all()

# User model mutations

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

        is_voter = Voter.objects.get(user=user)

        if is_voter:

            raise Exception("You cannot register as an organizer. You already have a voters account")

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

        return CreateOrganizer(organizer=organizer)

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    register_organizer = CreateOrganizer.Field()