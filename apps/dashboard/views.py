from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.games.models.userGameLibrary import UserGameLibrary
from django.db.models import Count, Q

from apps.games.models.game import Game
from apps.games.models.genre import Genre
from apps.games.models.review import Review
from apps.games.models.news import News

from django.utils import timezone

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
    
    new_releases = (
        Game.objects
        .filter(
            release_date__lte=timezone.localdate(),
            is_active=True,
        )
        .exclude(release_date__isnull=True)
        .order_by("-release_date")[:3]
    )
    
    upcoming_releases = (
        Game.objects
        .filter(
            release_date__gt=timezone.localdate(),
            is_active=True,
        )
        .exclude(release_date__isnull=True)
        .order_by("release_date")[:3]
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
    
    latest_library_game = (
        UserGameLibrary.objects
        .filter(user=request.user)
        .select_related("game")
        .order_by("-added_at")
        .first()
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
    
    recent_activities = []

    for entry in (
        UserGameLibrary.objects
        .filter(user=request.user)
        .select_related("game")
    ):

        recent_activities.append({
            "type": "library",
            "game": entry.game,
            "date": entry.added_at,
        })


    for review in (
        Review.objects
        .filter(user=request.user)
        .select_related("game")
    ):

        recent_activities.append({
            "type": "review",
            "game": review.game,
            "date": review.created_at,
        })


    recent_activities.sort(
        key=lambda activity: activity["date"],
        reverse=True,
    )

    recent_activities = recent_activities[:4]


    return render(
        request,
        "dashboard/dashboard_home.html",
        {
            "keep_exploring": keep_exploring,
            "recommendations": recommendations,
            "latest_library_game": latest_library_game,
            "new_releases": new_releases,
            "upcoming_releases": upcoming_releases,
            "recent_activities": recent_activities,
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