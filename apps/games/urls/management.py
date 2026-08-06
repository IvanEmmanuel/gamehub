from django.urls import path
from apps.games.views.management import (
    GameListView,
    GameManagementView,
)

app_name = 'gestion' #es un tipo de namespace

urlpatterns = [
    path('games', name='games')
]
