from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView

from ..models import Game
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ModerationRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user

        return (
            user.is_superuser
            or user.groups.filter(name="Moderador").exists()
        )

class GameManageView(ModerationRequiredMixin, DetailView):

    model = Game

    template_name = "games/management/game_manage.html"

    context_object_name = "game"
    
    # queryset = Game.objects.prefetch_related(
    #     "trailers",
    #     "screenshots",
    #     "achievements",
    #     "soundtracks",
    #     "guides",
    #     "dlcs",
    #     "patch_notes",
    # )