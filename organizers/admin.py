from django.contrib import admin
from .models import Organizer, Workspace

# Register your models here.
@admin.register(Organizer)
class OrganizerAdminView(admin.ModelAdmin):

    model = Organizer

    list_display = (
        'user',
        'paid_status',
        'running_package',
    )

    list_filter = (
        'created_date',
        'updated_date',
    )

@admin.register(Workspace)
class WorkspaceAdminView(admin.ModelAdmin):

    model = Workspace

    list_display = (
        'name',
        'poll_limit',
        'voter_limit',
    )

    list_filter = (
        'created_date',
        'updated_date',
    )