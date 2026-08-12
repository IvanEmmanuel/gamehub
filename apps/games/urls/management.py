from django.urls import path
from ..views.management import ( GameManageView, GameTrailerListView, GameTrailerCreateView, GameTrailerUpdateView, 
                                GameTrailerDeleteView, GameTrailerReorderView, GameScreenshotListView, GameScreenshotReorderView,
                                GameScreenshotCreateView, GameScreenshotUpdateView, GameScreenshotDeleteView, GameAchievementListView,
                                GameAchievementCreateView, GameAchievementUpdateView, GameAchievementDeleteView, GameAchievementReorderView,
                                GameSoundtrackListView,GameSoundtrackCreateView, GameSoundtrackUpdateView,GameSoundtrackDeleteView, GameSoundtrackReorderView,
                                GameDLCListView, GameDLCCreateView, GameDLCUpdateView, GameDLCDeleteView,GameDLCReorderView
                                )



app_name = "management"

urlpatterns = [
    path("games/<int:pk>/manage/", GameManageView.as_view(), name="game_manage",),
    path("games/<int:pk>/trailers/", GameTrailerListView.as_view(), name="game_trailer_list",),
    path("games/<int:pk>/trailers/create/", GameTrailerCreateView.as_view(), name="game_trailer_create",),
    path("games/<int:pk>/trailers/<int:trailer_id>/edit/", GameTrailerUpdateView.as_view(), name="game_trailer_update",),
    path("games/<int:pk>/trailers/<int:trailer_id>/delete/", GameTrailerDeleteView.as_view(), name="game_trailer_delete",),
    path("games/<int:pk>/trailers/reorder/", GameTrailerReorderView.as_view(), name="game_trailer_reorder",),
    path("games/<int:pk>/screenshots/", GameScreenshotListView.as_view(), name="game_screenshot_list",),
    path("games/<int:pk>/screenshots/reorder/", GameScreenshotReorderView.as_view(), name="game_screenshot_reorder",),
    path("games/<int:pk>/screenshots/create/", GameScreenshotCreateView.as_view(), name="game_screenshot_create",),
    path("games/<int:pk>/screenshots/<int:screenshot_id>/edit/", GameScreenshotUpdateView.as_view(), name="game_screenshot_update",),
    path("games/<int:pk>/screenshots/<int:screenshot_id>/delete/", GameScreenshotDeleteView.as_view(), name="game_screenshot_delete",),
    path("games/<int:pk>/achievements/", GameAchievementListView.as_view(), name="game_achievement_list",),
    path("games/<int:pk>/achievements/create/", GameAchievementCreateView.as_view(), name="game_achievement_create",),
    path("games/<int:pk>/achievements/<int:achievement_id>/edit/", GameAchievementUpdateView.as_view(), name="game_achievement_update",),
    path("games/<int:pk>/achievements/<int:achievement_id>/delete/", GameAchievementDeleteView.as_view(), name="game_achievement_delete",),
    path("games/<int:pk>/achievements/reorder/", GameAchievementReorderView.as_view(), name="game_achievement_reorder",),
    path("games/<int:pk>/soundtrack/", GameSoundtrackListView.as_view(), name="game_soundtrack_list",),
    path("games/<int:pk>/soundtrack/create/", GameSoundtrackCreateView.as_view(), name="game_soundtrack_create",),
    path("games/<int:pk>/soundtrack/<int:soundtrack_id>/edit/", GameSoundtrackUpdateView.as_view(), name="game_soundtrack_update",),
    path("games/<int:pk>/soundtrack/<int:soundtrack_id>/delete/", GameSoundtrackDeleteView.as_view(), name="game_soundtrack_delete",),
    path("games/<int:pk>/soundtrack/reorder/", GameSoundtrackReorderView.as_view(), name="game_soundtrack_reorder",),
    path("games/<int:pk>/dlcs/", GameDLCListView.as_view(), name="game_dlc_list",),
    path("games/<int:pk>/dlcs/create/", GameDLCCreateView.as_view(), name="game_dlc_create",),
    path("games/<int:pk>/dlcs/<int:dlc_id>/edit/", GameDLCUpdateView.as_view(), name="game_dlc_update",),
    path("games/<int:pk>/dlcs/<int:dlc_id>/delete/", GameDLCDeleteView.as_view(), name="game_dlc_delete",),
    path("games/<int:pk>/dlcs/reorder/", GameDLCReorderView.as_view(), name="game_dlc_reorder",),
]