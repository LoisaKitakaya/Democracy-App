from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import views

urlpatterns = [
    path('create_account/', views.create_account),
]

urlpatterns = format_suffix_patterns(urlpatterns)