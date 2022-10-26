from django.urls import path
from . import views

urlpatterns = [
    path('upload_avatar/', views.update_avatar)
]