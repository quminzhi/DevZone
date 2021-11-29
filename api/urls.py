from django.urls import path
from . import views

urlpatterns = [
    path('remove-tag/', views.removeTag),
]
