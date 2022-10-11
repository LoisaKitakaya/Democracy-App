from users.models import User
from organizers.models import Organizer, Workspace
from voters.models import Voter
from polls.models import Poll
from ballot.models import Ballot
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, OrganizerSerializer, WorkspaceSerializer

@csrf_exempt
@api_view(['POST'])
def create_account(request, format=None):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response({'Action status': 'Account created successfully.'}, status=status.HTTP_201_CREATED)

    return Response({'Action status': 'Error.'}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)