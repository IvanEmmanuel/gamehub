
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from ..models import (
    Game,
    Trailer,
    Screenshot,
    Achievement,
    Guide,
    DLC,
    Soundtrack,
    PatchNote,
    Genre,
)
from django.urls import reverse, reverse_lazy
from ..forms import GameForm



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

        queryset = Game.objects.all()

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )
            
        genre = self.request.GET.get("genre")

        if genre:
            queryset = queryset.filter(
                genres__id=genre
            )
            
        platform = self.request.GET.get("platform")

        if platform:
            queryset = queryset.filter(
                platforms__icontains=platform
            )
            
        order = self.request.GET.get("order")

        if order == "name_asc":
            queryset = queryset.order_by("name")

        elif order == "name_desc":
            queryset = queryset.order_by("-name")

        elif order == "newest":
            queryset = queryset.order_by("-release_date")

        elif order == "oldest":
            queryset = queryset.order_by("release_date")

        return queryset
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        
        context["genres"] = Genre.objects.filter(is_active=True).order_by("name")

        context["games_count"] = Game.objects.count()
        context["trailers_count"] = Trailer.objects.count()
        context["screenshots_count"] = Screenshot.objects.count()
        context["achievements_count"] = Achievement.objects.count()
        context["guides_count"] = Guide.objects.count()
        context["dlcs_count"] = DLC.objects.count()
        context["soundtracks_count"] = Soundtrack.objects.count()
        context["patch_notes_count"] = PatchNote.objects.count()

        return context
    
class GameCreateView(ModerationRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'games/moderation/game_form.html'
    success_url = reverse_lazy('moderation:game_list')
    
class GameUpdateView(ModerationRequiredMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'games/moderation/game_form.html'
    success_url = reverse_lazy('moderation:game_list')
    
    def form_valid(self, form):

        if self.request.POST.get("cover_clear") == "1":
            self.object.cover.delete(save=False)
            self.object.cover = None

        if self.request.POST.get("banner_clear") == "1":
            self.object.banner.delete(save=False)
            self.object.banner = None

        self.object.save()

        return super().form_valid(form)
    