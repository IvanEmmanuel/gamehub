from django.urls import path
from ..views.moderation import GameListView

app_name = 'moderation' #es un tipo de namespace

urlpatterns = [
    path('games/', GameListView.as_view(), name="game_list")
]
