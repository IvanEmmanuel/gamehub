from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from ..models import Game, Trailer
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms import TrailerForm
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.db import transaction
from django.views import View


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
    
class GameTrailerListView(ModerationRequiredMixin, DetailView,):

    model = Game

    template_name = "games/management/trailers/trailer_list.html"

    context_object_name = "game"
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["trailer_form"] = TrailerForm()

        return context
    
class GameTrailerCreateView(ModerationRequiredMixin, CreateView):

    model = Trailer
    form_class = TrailerForm

    def form_valid(self, form):

        form.instance.game_id = self.kwargs["pk"]

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "management:game_trailer_list",
            kwargs={"pk": self.kwargs["pk"]}
        )

class GameTrailerUpdateView(ModerationRequiredMixin, UpdateView):

    model = Trailer

    form_class = TrailerForm
    
    pk_url_kwarg = "trailer_id"

    def get_success_url(self):

        return reverse_lazy(
            "management:game_trailer_list",
            kwargs={"pk": self.object.game.pk}
        )
        
class GameTrailerDeleteView(ModerationRequiredMixin, DeleteView,):

    model = Trailer
    
    pk_url_kwarg = "trailer_id"

    def get_success_url(self):

        return reverse_lazy(
            "management:game_trailer_list",
            kwargs={"pk": self.object.game.pk}
        )
        
class GameTrailerReorderView(ModerationRequiredMixin, View):

    def post(self, request, pk):

        trailer_ids = request.POST.getlist("trailer_ids[]")

        if not trailer_ids:
            return JsonResponse(
                {
                    "success": False,
                    "error": "No se recibió ningún tráiler."
                },
                status=400
            )

        trailers = Trailer.objects.filter(
            game_id=pk,
            id__in=trailer_ids
        )

        trailers_by_id = {
            str(trailer.id): trailer
            for trailer in trailers
        }

        # Verificamos que todos los trailers pertenezcan al juego
        if len(trailers_by_id) != len(trailer_ids):

            return JsonResponse(
                {
                    "success": False,
                    "error": "Uno o más trailers no pertenecen a este juego."
                },
                status=400
            )

        with transaction.atomic():

            for position, trailer_id in enumerate(trailer_ids, start=1):

                trailer = trailers_by_id[trailer_id]

                trailer.display_order = position

            Trailer.objects.bulk_update(
                trailers_by_id.values(),
                ["display_order"]
            )

        return JsonResponse({
            "success": True
        })