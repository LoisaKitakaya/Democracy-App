from django.contrib import admin
from .models import Ballot
# Register your models here.
@admin.register(Ballot)
class VotesAdminView(admin.ModelAdmin):

    model = Ballot