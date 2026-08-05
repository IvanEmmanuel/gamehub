from django.urls import path

from ..views.public import (
    games_list,
    games_detail,
    games_content,
)

urlpatterns = [
    path("", games_list, name="games_list"),
    path("detail/<str:slug>/", games_detail, name="games_detail"),
    path("<str:slug>/content/", games_content, name="games_content"),
]