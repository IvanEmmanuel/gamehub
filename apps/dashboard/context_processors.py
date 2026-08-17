from django.utils import timezone

from apps.games.models.game import Game
from apps.games.models.review import Review
from apps.games.models.userGameLibrary import UserGameLibrary


def dashboard_sidebar(request):

    if not request.user.is_authenticated:
        return {}

    # ==========================================
    # NUEVOS LANZAMIENTOS
    # ==========================================

    new_releases = (
        Game.objects
        .filter(
            release_date__lte=timezone.localdate(),
            is_active=True,
        )
        .exclude(
            release_date__isnull=True
        )
        .order_by("-release_date")[:3]
    )


    # ==========================================
    # PRÓXIMOS LANZAMIENTOS
    # ==========================================

    upcoming_releases = (
        Game.objects
        .filter(
            release_date__gt=timezone.localdate(),
            is_active=True,
        )
        .exclude(
            release_date__isnull=True
        )
        .order_by("release_date")[:3]
    )


    # ==========================================
    # ACTIVIDAD RECIENTE
    # ==========================================

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


    return {
        "recent_activities": recent_activities,
        "new_releases": new_releases,
        "upcoming_releases": upcoming_releases,
    }