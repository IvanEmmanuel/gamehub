from django.urls import path

from ..views.public import (
    games_list,
    games_detail,
    games_content,
    my_library,
    add_to_library,
    remove_from_library,
    review_game,
)

app_name = "public"

urlpatterns = [
    path("", games_list, name="games_list"),
    path("detail/<str:slug>/", games_detail, name="games_detail"), # tambien implementada para renderizar reviews
    path("<str:slug>/content/", games_content, name="games_content"),
    path("library/", my_library, name="my_library"),
    path("detail/<str:slug>/library/add/", add_to_library, name="add_to_library",),
    path("detail/<str:slug>/library/remove/", remove_from_library, name="remove_from_library",),
    path("<slug:slug>/review/", review_game, name="review_game"),
]