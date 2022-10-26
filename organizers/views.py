from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Organizer

# Create your views here.

@api_view(['POST'])
def update_avatar(request):

    id = request.data.get("id")
    image = request.FILES.get('image')

    try:

        organizer = Organizer.objects.get(id=int(id))

    except:

        print("organizer account does not exist")

        return Response(data={"error": "account by that id does not exist"}, status=status.HTTP_404_NOT_FOUND)

    else:

        organizer.image = image

        organizer.save()

        return Response(data={"success": "avatar updated"}, status=status.HTTP_200_OK)

