from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Candidate

# Create your views here.

@api_view(['POST'])
def update_avatar(request, format=None):

    id = request.data.get("id")
    image = request.FILES.get('image')

    try:

        candidate = Candidate.objects.get(id=int(id))

    except:

        print("candidate account does not exist")

        return Response(data={"error": "account by that id does not exist"}, status=status.HTTP_404_NOT_FOUND)

    else:

        candidate.image = image

        candidate.save()

        return Response(data={"success": "avatar updated"}, status=status.HTTP_200_OK)