from django.urls import path

from gameapi.views import game, games

urlpatterns = [
    path('games/', games, name='games'),
    path('game/<str:game_id>/', game, name='game'),
]
