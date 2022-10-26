from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('upload_avatar/', views.update_avatar)
]

urlpatterns = format_suffix_patterns(urlpatterns)