from django.urls import path

from gameapi.views import games

urlpatterns = [
    path('games/', games, name='games'),
]
