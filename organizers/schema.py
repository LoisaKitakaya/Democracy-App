import graphene
from graphene_django import DjangoObjectType
from organizers.models import Organizer, Workspace

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

        return Organizer.objects.all()

    def resolve_all_workspaces(root, info):

        return Workspace.objects.all()

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    pass