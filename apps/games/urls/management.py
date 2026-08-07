from django.urls import path
from ..views.management import GameManageView

app_name = "management"

urlpatterns = [
    path("games/<int:pk>/manage/", GameManageView.as_view(), name="game_manage",),
]