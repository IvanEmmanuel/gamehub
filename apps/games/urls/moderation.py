from django.urls import path
from ..views.moderation import GameListView, GameCreateView, GameUpdateView,GameDeleteView

app_name = 'moderation' #es un tipo de namespace

urlpatterns = [
    path('games/', GameListView.as_view(), name="game_list"),
    path('games/create', GameCreateView.as_view(), name="game_create"),
    path("games/<int:pk>/edit/", GameUpdateView.as_view(), name="game_update",
    ),

    path("games/<int:pk>/delete/", GameDeleteView.as_view(), name="game_delete", ),

    # path(
    #     "games/<int:pk>/manage/",
    #     GameManageView.as_view(),
    #     name="game_manage",
    # ),
]
