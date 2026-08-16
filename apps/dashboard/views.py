from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.games.models.userGameLibrary import UserGameLibrary
from django.db.models import Count, Q

from apps.games.models.game import Game
from apps.games.models.genre import Genre

# Create your views here.

@login_required
def dashboard_home(request):

    # ==========================================
    # JUEGOS DE LA BIBLIOTECA
    # ==========================================

    library_games = (
        UserGameLibrary.objects
        .filter(user=request.user)
        .values_list("game_id", flat=True)
    )


    # ==========================================
    # GÉNEROS DE LA BIBLIOTECA DEL USUARIO
    # ==========================================

    user_genres = (
        Genre.objects
        .filter(
            games__usergamelibrary__user=request.user,
            is_active=True,
        )
        .distinct()
    )


    # ==========================================
    # RECOMENDACIONES
    # ==========================================

    recommendations = (
        Game.objects
        .filter(
            genres__in=user_genres,
            is_active=True,
        )
        .exclude(
            id__in=library_games
        )
        .annotate(
            matching_genres=Count(
                "genres",
                filter=Q(
                    genres__in=user_genres,
                    genres__is_active=True,
                ),
                distinct=True,
            )
        )
        .order_by(
            "-matching_genres",
            "-created_at",
        )[:6]
    )


    # ==========================================
    # CONTINÚA EXPLORANDO
    # ==========================================

    keep_exploring = (
        UserGameLibrary.objects
        .filter(user=request.user)
        .select_related("game")
        .prefetch_related("game__genres")
        .order_by("?")[:3]
    )


    return render(
        request,
        "dashboard/dashboard_home.html",
        {
            "keep_exploring": keep_exploring,
            "recommendations": recommendations,
        }
    )

@login_required
def dashboard_profile(request):
    return render(
        request,
        "dashboard/dashboard_profile.html"
    )

def redirect_home(request):
    return redirect('public:games_list')

@login_required
def dashboard_library(request):

    library_entries = (
        UserGameLibrary.objects
        .filter(user=request.user)
        .select_related("game")
        .prefetch_related("game__genres")
        .order_by("-added_at")
    )

    return render(
        request,
        "dashboard/dashboard_library.html",
        {
            "library_entries": library_entries,
        }
    )