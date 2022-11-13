from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Organizer

# Create your views here.

@api_view(['GET', 'POST'])
def avatar(request):

    if request.method == 'GET':

        id = request.GET['id']

        try:

            organizer = Organizer.objects.get(id=int(id))

        except:

            print("organizer account does not exist")

            return Response(data={"error": "account by that id does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:

            organizer.image.url

        except:

            print("organizer does not have an existing avatar")

            return Response(data={"image": "https://via.placeholder.com/720x468"}, status=status.HTTP_200_OK)

        else:

            return Response(data={"image": organizer.image.url}, status=status.HTTP_200_OK)

    if request.method == 'POST':

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

