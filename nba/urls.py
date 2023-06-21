from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('team/list', views.team_list, name='team_list'),
    path('team/<str:team_id>', views.team, name='team'),
    path('player/list', views.player_list, name='player_list'),
    path('player/<str:player_id>', views.player, name='player'),
    path('game/list', views.game_list, name='game_list'),
    path('game/list/<slug:season_id>', views.game_list, name='game_list'),
    path('game/list/<slug:season_id>/<str:month>', views.game_list, name='game_list'),
    path('game/<str:game_id>', views.game, name='game'),
    path('standings', views.standings, name='standings'),
    path('standings/<slug:season_id>', views.standings, name='standings'),
]