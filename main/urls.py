from django.urls import path
from . import api

urlpatterns = [
    path('data/', api.api),
]
