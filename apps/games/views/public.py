from django.shortcuts import render, get_object_or_404, redirect
from ..models.game import Game
from ..models.genre import Genre
from ..models.review import Review
from ..forms import ReviewForm
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from ..models.userGameLibrary import UserGameLibrary
from django.views.decorators.http import require_POST
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages

# Create your views here.


def games_list(request):
    
    games = (
        Game.objects
        .filter(is_active=True)
        .prefetch_related("genres")
    )
    
    library_game_ids = set()

    if request.user.is_authenticated:

        library_game_ids = set(
            UserGameLibrary.objects
            .filter(user=request.user)
            .values_list("game_id", flat=True)
        )
        
    library_entries = []

    if request.user.is_authenticated:

        library_entries = (
            UserGameLibrary.objects
            .filter(user=request.user)
            .select_related("game")
            .prefetch_related("game__genres")
            .order_by("-added_at")[:3]
        )
    
    genres = Genre.objects.all()
    
    query = request.GET.get("q", "").strip()
    
    selected_genres = request.GET.getlist("genre")
    selected_platforms = request.GET.getlist("platform")
    selected_statuses = request.GET.getlist("status")
    selected_order = request.GET.get("order", "recent")
    multiplayer = request.GET.get("multiplayer")
    new_releases = request.GET.get("new_releases")
    popular = request.GET.get("popular")
    
    has_filters = bool(
        query
        or selected_genres
        or selected_platforms
        or selected_statuses
        or multiplayer
        or new_releases
        or popular
    )
    
    
    if query:
        games = games.filter(
            Q(name__icontains=query) |
            Q(developer__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()
        
        
    if selected_genres:

        games = games.filter(
            genres__id__in=selected_genres
        ).distinct()
        
        
    if selected_platforms:

        platform_query = Q()

        for platform in selected_platforms:

            platform_query |= Q(
                platforms__icontains=platform
            )

        games = games.filter(platform_query)
        
    
    if selected_statuses:

        games = games.filter(
            status__in=selected_statuses
        )
        
    if multiplayer == "true":

        games = games.filter(
            has_multiplayer=True
        )
        
    if new_releases == "true":

        today = timezone.localdate()

        ninety_days_ago = today - timedelta(days=90)

        games = games.filter(
            release_date__gte=ninety_days_ago,
            release_date__lte=today
        )
        
    if popular == "true":

        games = games.annotate(
            library_count=Count("usergamelibrary")
        ).order_by("-library_count", "name")
        
        
        
        
    if popular == "true":

        games = games.order_by(
            "-library_count",
            "name"
        )

    elif new_releases == "true":

        games = games.order_by(
            "-release_date"
        )

    elif selected_order == "recent":

        games = games.order_by("-created_at")

    elif selected_order == "oldest":

        games = games.order_by("created_at")

    elif selected_order == "name_asc":

        games = games.order_by("name")

    elif selected_order == "name_desc":

        games = games.order_by("-name")
        
        
    paginator = Paginator(games, 12)
    page_number = request.GET.get("page")
    games_obj = paginator.get_page(page_number)
    
    query_params = request.GET.copy()
    
    if "page" in query_params:
        query_params.pop("page")
    
    query_string = query_params.urlencode()
    
    return render(request, "games/games.html", {
        'games_obj': games_obj,
        'query': query,
        'query_string': query_string,
        'genres': genres,
        "selected_genres": selected_genres,
        "selected_platforms": selected_platforms,
        "selected_statuses": selected_statuses,
        "selected_order": selected_order,
        "library_game_ids": library_game_ids,
        "library_entries": library_entries,
        "has_filters": has_filters,
    })

def games_detail(request, slug):

    game = get_object_or_404(Game, slug=slug)

    is_in_library = (
        request.user.is_authenticated
        and UserGameLibrary.objects.filter(
            user=request.user,
            game=game,
        ).exists()
    )

    reviews = (
        Review.objects
        .filter(game=game)
        .select_related("user", "user__userprofile")
        .order_by("-created_at")
    )
    
    review_stats = Review.objects.filter(
        game=game
    ).aggregate(
        average=Avg("rating"),
        total=Count("id"),
    )
    
    average_rating = review_stats["average"] or 0

    full_stars = int(average_rating)
    has_half_star = (average_rating - full_stars) >= 0.5
    empty_stars = 5 - full_stars - int(has_half_star)
    
    

    rating_counts = (
        Review.objects
        .filter(game=game)
        .values("rating")
        .annotate(total=Count("id"))
    )

    rating_counts = {
        item["rating"]: item["total"]
        for item in rating_counts
    }

    rating_distribution = []

    for rating in range(5, 0, -1):

        total = rating_counts.get(rating, 0)

        percentage = (
            round((total / review_stats["total"]) * 100)
            if review_stats["total"]
            else 0
        )

        rating_distribution.append({
            "rating": rating,
            "total": total,
            "percentage": percentage,
        })

    user_review = None

    if request.user.is_authenticated:

        user_review = Review.objects.filter(
            user=request.user,
            game=game,
        ).first()

    review_form = ReviewForm(
        instance=user_review
    )

    return render(
        request,
        "games/games_detail.html",
        {
            "game": game,
            "is_in_library": is_in_library,
            "reviews": reviews,
            "review_form": review_form,
            "review_average": review_stats["average"],
            "review_total": review_stats["total"],
            "rating_distribution": rating_distribution,
            "user_review": user_review,
            "full_stars": full_stars,
            "has_half_star": has_half_star,
            "empty_stars": empty_stars,
        },
    )

def games_content(request, slug):

    game = get_object_or_404(

        Game.objects.prefetch_related(

            "trailers",
            "screenshots",
            "dlcs",
            "achievements",
            "soundtracks",

        ),

        slug=slug

    )

    return render(
        request,
        "games/games_content.html",
        {
            "game": game
        }
    )
    
@login_required
def my_library(request):
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
        },
    )
    
@login_required
@require_POST
def add_to_library(request, slug):
    game = get_object_or_404(
        Game,
        slug=slug,
        is_active=True,
    )

    UserGameLibrary.objects.get_or_create(
        user=request.user,
        game=game,
    )

    return redirect("public:my_library")

@login_required
@require_POST
def remove_from_library(request, slug):
    library_entry = get_object_or_404(
        UserGameLibrary,
        user=request.user,
        game__slug=slug,
    )

    library_entry.delete()

    return redirect("public:my_library")

@login_required
@require_POST
def review_game(request, slug):

    game = get_object_or_404(
        Game,
        slug=slug,
        is_active=True,
    )

    try:
        instance = Review.objects.get(
            user=request.user,
            game=game,
        )
        is_update = True

    except Review.DoesNotExist:
        instance = None
        is_update = False

    form = ReviewForm(
        request.POST,
        instance=instance,
    )

    if form.is_valid():

        review = form.save(commit=False)

        review.user = request.user
        review.game = game

        review.save()

        message = (
            "Reseña actualizada"
            if is_update
            else "Gracias por tu reseña"
        )

        messages.success(request, message)

        return redirect(
            "public:games_detail",
            slug=game.slug,
        )

    messages.error(
        request,
        "No se pudo guardar la reseña. Revisa los datos.",
    )

    return redirect(
        "public:games_detail",
        slug=game.slug,
    )