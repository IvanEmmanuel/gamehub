
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from ..models import Game


class ModerationRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user

        return (
            user.is_superuser
            or user.groups.filter(name="Moderador").exists()
        )
    
    
class GameListView(ModerationRequiredMixin, ListView):
    model = Game
    template_name = "games/moderation/game_list.html"
    context_object_name = "games"
    paginate_by = 10
    ordering = ["name"]
    
    def get_queryset(self):
        return Game.objects.all()