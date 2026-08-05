from django.urls import path
from games.views import moderation

app_name = 'gestion' #es un tipo de namespace

urlpatterns = [
    path('games', name='games')
]
