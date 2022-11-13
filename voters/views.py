from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Voter

# Create your views here.

@api_view(['GET', 'POST'])
def avatar(request):

    if request.method == 'GET':

        id = request.GET['id']

        try:

            voter = Voter.objects.get(id=int(id))

        except:

            print("voter account does not exist")

            return Response(data={"error": "account by that id does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:

            voter.image.url

        except:

            print("voter does not have an existing avatar")

            return Response(data={"image": "https://via.placeholder.com/720x468"}, status=status.HTTP_200_OK)

        else:

            return Response(data={"image": voter.image.url}, status=status.HTTP_200_OK)

    if request.method == 'POST':

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

