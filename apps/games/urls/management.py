from django.urls import path
from ..views.management import GameManageView, GameTrailerListView, GameTrailerCreateView, GameTrailerUpdateView, GameTrailerDeleteView, GameTrailerReorderView

app_name = "management"

urlpatterns = [
    path("games/<int:pk>/manage/", GameManageView.as_view(), name="game_manage",),
    path("games/<int:pk>/trailers/", GameTrailerListView.as_view(), name="game_trailer_list",),
    path("games/<int:pk>/trailers/create/", GameTrailerCreateView.as_view(), name="game_trailer_create",),
    path("games/<int:pk>/trailers/<int:trailer_id>/edit/", GameTrailerUpdateView.as_view(), name="game_trailer_update",),
    path("games/<int:pk>/trailers/<int:trailer_id>/delete/", GameTrailerDeleteView.as_view(), name="game_trailer_delete",),
    path("games/<int:pk>/trailers/reorder/", GameTrailerReorderView.as_view(), name="game_trailer_reorder",),
]