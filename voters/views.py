from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Voter

# Create your views here.

@api_view(['POST'])
def update_avatar(request):

    id = request.data.get("id")
    image = request.FILES.get('image')

    try:

        voter = Voter.objects.get(id=int(id))

    except:

        print("voter account does not exist")

        return Response(data={"error": "account by that id does not exist"}, status=status.HTTP_404_NOT_FOUND)

    else:

        voter.image = image

        voter.save()

        return Response(data={"success": "avatar updated"}, status=status.HTTP_200_OK)

