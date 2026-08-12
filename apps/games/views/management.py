from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from ..models import Game, Trailer, Screenshot
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms import TrailerForm, ScreenshotForm
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.db import transaction
from django.views import View
from django.shortcuts import get_object_or_404

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
        
class GameScreenshotListView(ModerationRequiredMixin, DetailView,):

    model = Game

    template_name = "games/management/screenshots/screenshot_list.html"

    context_object_name = "game"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["screenshot_form"] = ScreenshotForm()

        return context
    
class GameScreenshotReorderView(ModerationRequiredMixin, View,):

    def post(self, request, pk):

        screenshot_ids = request.POST.getlist(
            "screenshot_ids[]"
        )

        if not screenshot_ids:

            return JsonResponse(
                {
                    "success": False,
                    "error": "No se recibió ningún screenshot."
                },
                status=400
            )

        screenshots = Screenshot.objects.filter(
            game_id=pk,
            id__in=screenshot_ids
        )

        screenshots_by_id = {
            str(screenshot.id): screenshot
            for screenshot in screenshots
        }

        # Verificar que todos pertenezcan al juego
        if len(screenshots_by_id) != len(screenshot_ids):

            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "Uno o más screenshots "
                        "no pertenecen a este juego."
                    )
                },
                status=400
            )

        with transaction.atomic():

            for position, screenshot_id in enumerate(
                screenshot_ids,
                start=1
            ):

                screenshot = screenshots_by_id[screenshot_id]

                screenshot.display_order = position

            Screenshot.objects.bulk_update(
                screenshots_by_id.values(),
                ["display_order"]
            )

        return JsonResponse({
            "success": True
        })
        
class GameScreenshotCreateView(ModerationRequiredMixin, CreateView):

    model = Screenshot
    form_class = ScreenshotForm

    def form_valid(self, form):

        if not form.cleaned_data.get("image"):

            form.add_error(
                "image",
                "Debes seleccionar una imagen."
            )

            return self.form_invalid(form)

        form.instance.game_id = self.kwargs["pk"]

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "management:game_screenshot_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
        
class GameScreenshotUpdateView(ModerationRequiredMixin, UpdateView):

    model = Screenshot
    form_class = ScreenshotForm

    def get_object(self, queryset=None):

        return get_object_or_404(
            Screenshot,
            id=self.kwargs["screenshot_id"],
            game_id=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        return JsonResponse({
            "id": self.object.id,
            "title": self.object.title,
            "image": self.object.image.url if self.object.image else "",
        })

    def get_success_url(self):

        return reverse_lazy(
            "management:game_screenshot_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
        
class GameScreenshotDeleteView(ModerationRequiredMixin, DeleteView):

    model = Screenshot

    def get_object(self, queryset=None):

        return get_object_or_404(
            Screenshot,
            id=self.kwargs["screenshot_id"],
            game_id=self.kwargs["pk"]
        )

    def get_success_url(self):

        return reverse_lazy(
            "management:game_screenshot_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
        
