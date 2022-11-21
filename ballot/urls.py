from django.urls import path
from . import views

urlpatterns = [
    path('pdf/<int:id>/', views.generate_report)
]