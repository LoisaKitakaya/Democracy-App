import graphene
from django.http import HttpRequest as request
from graphene_file_upload.scalars import Upload
from graphene_django import DjangoObjectType
from organizers.models import Organizer, Workspace
from organizers.forms import UploadOrganizerForm
from users.models import User

# my object type

class UserType(DjangoObjectType):

    class Meta:

        model = User

        fields = '__all__'

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

        user_id = graphene.Int(required=True)
        phone = graphene.String(required=True)
        country = graphene.String(required=True)
        # image = Upload(required=False)

    organizer = graphene.Field(OrganizerType)

    @classmethod
    def mutate(
        cls, root, info,
        user_id,
        phone,
        country,
        # image
    ):

        user = User.objects.get(id=user_id)

        organizer = Organizer.objects.create(
            user=user,
            phone=phone,
            country=country
        )

        if request.method == 'POST':

            form = UploadOrganizerForm(request.FILES, instance=organizer)

            if form.is_valid():

                form.save

        return CreateOrganizer(organizer=organizer)

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    register_organizer = CreateOrganizer.Field()