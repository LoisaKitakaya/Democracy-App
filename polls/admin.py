from django.contrib import admin
from .models import Poll, Candidate

# Register your models here.
@admin.register(Poll)
class PollsAdminView(admin.ModelAdmin):

    model = Poll

    list_display = (
        'seat',
        'begin_date',
        'end_date',
    )

    list_filter = (
        'created_date',
        'updated_date',
    )

@admin.register(Candidate)
class CandidateAdminView(admin.ModelAdmin):

    model = Candidate

    list_display = (
        'first_name',
        'last_name',
        'email',
    )

    list_filter = (
        'created_date',
        'updated_date',
    )