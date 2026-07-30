from django.urls import path
from . import views

urlpatterns = [
    path("", views.games_list, name="games_list"),  # /games
    path("detail/", views.games_detail, name="games_detail"),
    path("content/", views.games_content, name="games_content")
]
