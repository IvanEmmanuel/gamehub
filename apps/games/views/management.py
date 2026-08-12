from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from ..models import Game, Trailer, Screenshot, Achievement, Soundtrack, DLC, Guide, PatchNote
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from ..forms import TrailerForm, ScreenshotForm, AchievementForm, SoundtrackForm, DLCForm, GuideForm, PatchNoteForm
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
        
class GameAchievementListView(ModerationRequiredMixin, ListView):

    model = Achievement
    template_name = "games/management/achievements/achievement_list.html"
    context_object_name = "achievements"

    def get_queryset(self):

        return Achievement.objects.filter(
            game_id=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["game"] = get_object_or_404(
            Game,
            pk=self.kwargs["pk"]
        )

        return context
    
class GameAchievementCreateView(ModerationRequiredMixin, CreateView):

    model = Achievement
    form_class = AchievementForm

    def form_valid(self, form):

        form.instance.game_id = self.kwargs["pk"]

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "management:game_achievement_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
        
class GameAchievementUpdateView(ModerationRequiredMixin, UpdateView):

    model = Achievement
    form_class = AchievementForm

    def get_object(self, queryset=None):

        return get_object_or_404(
            Achievement,
            id=self.kwargs["achievement_id"],
            game_id=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        return JsonResponse({
            "id": self.object.id,
            "title": self.object.title,
            "description": self.object.description,
            "icon": (
                self.object.icon.url
                if self.object.icon
                else ""
            ),
            "is_hidden": self.object.is_hidden,
        })

    def get_success_url(self):

        return reverse_lazy(
            "management:game_achievement_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
        
class GameAchievementDeleteView(ModerationRequiredMixin, DeleteView):

    model = Achievement

    def get_object(self, queryset=None):

        return get_object_or_404(
            Achievement,
            id=self.kwargs["achievement_id"],
            game_id=self.kwargs["pk"]
        )

    def get_success_url(self):

        return reverse_lazy(
            "management:game_achievement_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
    
class GameAchievementReorderView(ModerationRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        game_id = kwargs["pk"]

        achievement_ids = request.POST.getlist(
            "achievement_ids[]"
        )

        achievements = Achievement.objects.filter(
            game_id=game_id,
            id__in=achievement_ids
        )

        achievements_by_id = {
            str(achievement.id): achievement
            for achievement in achievements
        }

        for index, achievement_id in enumerate(
            achievement_ids,
            start=1
        ):

            achievement = achievements_by_id.get(
                achievement_id
            )

            if achievement:

                achievement.display_order = index

                achievement.save(
                    update_fields=["display_order"]
                )

        return JsonResponse({
            "success": True
        })
        
class GameSoundtrackListView(ModerationRequiredMixin, ListView):

    model = Soundtrack
    template_name = "games/management/soundtracks/soundtrack_list.html"
    context_object_name = "soundtracks"

    def get_queryset(self):

        return Soundtrack.objects.filter(
            game_id=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["game"] = get_object_or_404(
            Game,
            pk=self.kwargs["pk"]
        )

        return context
    
class GameSoundtrackCreateView(ModerationRequiredMixin, CreateView):

    model = Soundtrack
    form_class = SoundtrackForm

    def form_valid(self, form):

        form.instance.game_id = self.kwargs["pk"]

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "management:game_soundtrack_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
        
class GameSoundtrackUpdateView(ModerationRequiredMixin, UpdateView):

    model = Soundtrack
    form_class = SoundtrackForm

    def get_object(self, queryset=None):

        return get_object_or_404(
            Soundtrack,
            id=self.kwargs["soundtrack_id"],
            game_id=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        return JsonResponse({
            "id": self.object.id,
            "title": self.object.title,
            "artist": self.object.artist,
            "spotify_url": self.object.spotify_url,
            "youtube_url": self.object.youtube_url,
        })

    def get_success_url(self):

        return reverse_lazy(
            "management:game_soundtrack_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
        
class GameSoundtrackDeleteView(ModerationRequiredMixin, DeleteView):

    model = Soundtrack

    def get_object(self, queryset=None):

        return get_object_or_404(
            Soundtrack,
            id=self.kwargs["soundtrack_id"],
            game_id=self.kwargs["pk"]
        )

    def get_success_url(self):

        return reverse_lazy(
            "management:game_soundtrack_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
        
class GameSoundtrackReorderView(ModerationRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        game_id = kwargs["pk"]

        soundtrack_ids = request.POST.getlist(
            "soundtrack_ids[]"
        )

        soundtracks = Soundtrack.objects.filter(
            game_id=game_id,
            id__in=soundtrack_ids
        )

        soundtracks_by_id = {
            str(soundtrack.id): soundtrack
            for soundtrack in soundtracks
        }

        for index, soundtrack_id in enumerate(
            soundtrack_ids,
            start=1
        ):

            soundtrack = soundtracks_by_id.get(
                soundtrack_id
            )

            if soundtrack:

                soundtrack.display_order = index

                soundtrack.save(
                    update_fields=["display_order"]
                )

        return JsonResponse({
            "success": True
        })
        
class GameDLCListView(ModerationRequiredMixin, ListView):

    model = DLC
    template_name = "games/management/dlcs/dlc_list.html"
    context_object_name = "dlcs"

    def get_queryset(self):

        return DLC.objects.filter(
            game_id=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["game"] = get_object_or_404(
            Game,
            pk=self.kwargs["pk"]
        )

        return context
    
class GameDLCCreateView(ModerationRequiredMixin, CreateView):

    model = DLC
    form_class = DLCForm

    def form_valid(self, form):

        form.instance.game_id = self.kwargs["pk"]

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "management:game_dlc_list",
            kwargs={"pk": self.kwargs["pk"]}
        )
        
class GameDLCUpdateView(ModerationRequiredMixin, UpdateView):

    model = DLC
    form_class = DLCForm

    def get_object(self, queryset=None):

        return get_object_or_404(
            DLC,
            id=self.kwargs["dlc_id"],
            game_id=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        return JsonResponse({
            "id": self.object.id,
            "title": self.object.title,
            "description": self.object.description,
            "type": self.object.type,
            "cover": (
                self.object.cover.url
                if self.object.cover
                else ""
            ),
            "release_date": (
                self.object.release_date.isoformat()
                if self.object.release_date
                else ""
            ),
            "purchase_url": self.object.purchase_url,
        })

    def form_valid(self, form):

        if not form.cleaned_data.get("cover"):

            form.instance.cover = self.get_object().cover

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "management:game_dlc_list",
            kwargs={
                "pk": self.kwargs["pk"]
            }
        )
        
class GameDLCDeleteView(ModerationRequiredMixin, DeleteView):

    model = DLC

    def get_object(self, queryset=None):

        return get_object_or_404(
            DLC,
            id=self.kwargs["dlc_id"],
            game_id=self.kwargs["pk"]
        )

    def get_success_url(self):

        return reverse_lazy(
            "management:game_dlc_list",
            kwargs={
                "pk": self.kwargs["pk"]
            }
        )
        
class GameDLCReorderView(ModerationRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        game_id = kwargs["pk"]

        dlc_ids = request.POST.getlist(
            "dlc_ids[]"
        )

        dlcs = DLC.objects.filter(
            game_id=game_id,
            id__in=dlc_ids
        )

        dlcs_by_id = {
            str(dlc.id): dlc
            for dlc in dlcs
        }

        for index, dlc_id in enumerate(
            dlc_ids,
            start=1
        ):

            dlc = dlcs_by_id.get(dlc_id)

            if dlc:

                dlc.display_order = index

                dlc.save(
                    update_fields=["display_order"]
                )

        return JsonResponse({
            "success": True
        })
        
class GameGuideListView(ModerationRequiredMixin, ListView):

    model = Guide
    template_name = "games/management/guides/guide_list.html"
    context_object_name = "guides"

    def get_queryset(self):

        return Guide.objects.filter(
            game_id=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["game"] = get_object_or_404(
            Game,
            pk=self.kwargs["pk"]
        )

        return context
    
class GameGuideCreateView(ModerationRequiredMixin, CreateView):

    model = Guide
    form_class = GuideForm

    def form_valid(self, form):

        form.instance.game_id = self.kwargs["pk"]

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "management:game_guide_list",
            kwargs={
                "pk": self.kwargs["pk"]
            }
        )
        
class GameGuideUpdateView(ModerationRequiredMixin, UpdateView):

    model = Guide
    form_class = GuideForm

    def get_object(self, queryset=None):

        return get_object_or_404(
            Guide,
            id=self.kwargs["guide_id"],
            game_id=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        return JsonResponse({
            "id": self.object.id,
            "title": self.object.title,
            "description": self.object.description,
            "url": self.object.url,
            "source": self.object.source,
        })

    def get_success_url(self):

        return reverse_lazy(
            "management:game_guide_list",
            kwargs={
                "pk": self.kwargs["pk"]
            }
        )
        
class GameGuideDeleteView(ModerationRequiredMixin, DeleteView):

    model = Guide

    def get_object(self, queryset=None):

        return get_object_or_404(
            Guide,
            id=self.kwargs["guide_id"],
            game_id=self.kwargs["pk"]
        )

    def get_success_url(self):

        return reverse_lazy(
            "management:game_guide_list",
            kwargs={
                "pk": self.kwargs["pk"]
            }
        )
        
class GameGuideReorderView(ModerationRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        game_id = kwargs["pk"]

        guide_ids = request.POST.getlist(
            "guide_ids[]"
        )

        guides = Guide.objects.filter(
            game_id=game_id,
            id__in=guide_ids
        )

        guides_by_id = {
            str(guide.id): guide
            for guide in guides
        }

        for index, guide_id in enumerate(
            guide_ids,
            start=1
        ):

            guide = guides_by_id.get(guide_id)

            if guide:

                guide.display_order = index

                guide.save(
                    update_fields=["display_order"]
                )

        return JsonResponse({
            "success": True
        })
        
class GamePatchNoteListView(ModerationRequiredMixin, ListView):

    model = PatchNote
    template_name = "games/management/patch_notes/patch_note_list.html"
    context_object_name = "patch_notes"

    def get_queryset(self):

        return PatchNote.objects.filter(
            game_id=self.kwargs["pk"]
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["game"] = get_object_or_404(
            Game,
            pk=self.kwargs["pk"]
        )

        return context
    
class GamePatchNoteCreateView(ModerationRequiredMixin, CreateView):

    model = PatchNote
    form_class = PatchNoteForm

    def form_valid(self, form):

        form.instance.game_id = self.kwargs["pk"]

        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy(
            "management:game_patch_note_list",
            kwargs={
                "pk": self.kwargs["pk"]
            }
        )
        
class GamePatchNoteUpdateView(ModerationRequiredMixin, UpdateView):

    model = PatchNote
    form_class = PatchNoteForm

    def get_object(self, queryset=None):

        return get_object_or_404(
            PatchNote,
            id=self.kwargs["patch_note_id"],
            game_id=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        return JsonResponse({
            "id": self.object.id,
            "version": self.object.version,
            "title": self.object.title,
            "description": self.object.description,
            "release_date": (
                self.object.release_date.isoformat()
                if self.object.release_date
                else ""
            ),
            "official_url": self.object.official_url,
        })

    def get_success_url(self):

        return reverse_lazy(
            "management:game_patch_note_list",
            kwargs={
                "pk": self.kwargs["pk"]
            }
        )
        
class GamePatchNoteDeleteView(ModerationRequiredMixin, DeleteView):

    model = PatchNote

    def get_object(self, queryset=None):

        return get_object_or_404(
            PatchNote,
            id=self.kwargs["patch_note_id"],
            game_id=self.kwargs["pk"]
        )

    def get_success_url(self):

        return reverse_lazy(
            "management:game_patch_note_list",
            kwargs={
                "pk": self.kwargs["pk"]
            }
        )
        
class GamePatchNoteReorderView(ModerationRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        game_id = kwargs["pk"]

        patch_note_ids = request.POST.getlist(
            "patch_note_ids[]"
        )

        patch_notes = PatchNote.objects.filter(
            game_id=game_id,
            id__in=patch_note_ids
        )

        patch_notes_by_id = {
            str(patch_note.id): patch_note
            for patch_note in patch_notes
        }

        for index, patch_note_id in enumerate(
            patch_note_ids,
            start=1
        ):

            patch_note = patch_notes_by_id.get(
                patch_note_id
            )

            if patch_note:

                patch_note.display_order = index

                patch_note.save(
                    update_fields=["display_order"]
                )

        return JsonResponse({
            "success": True
        })
        
