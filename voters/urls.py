from django.urls import path
from . import views

urlpatterns = [
    path('avatar/', views.avatar)
]