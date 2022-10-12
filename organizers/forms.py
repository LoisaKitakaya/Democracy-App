from django import forms
from organizers.models import Organizer

class UploadOrganizerForm(forms.ModelForm):

    class Meta:

        model = Organizer

        fields = ['image']