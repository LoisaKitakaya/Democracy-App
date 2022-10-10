from django.contrib import admin
from .models import Voter

# Register your models here.
@admin.register(Voter)
class VoterAdminView(admin.ModelAdmin):

    model = Voter

    list_display = (
        'user',
        'country',
    )

    list_filter = (
        'created_date',
        'updated_date',
    )