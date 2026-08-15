from django.shortcuts import render, get_object_or_404, redirect
from ..models.game import Game
from ..models.genre import Genre
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from ..models.userGameLibrary import UserGameLibrary
from django.views.decorators.http import require_POST


# Create your views here.


def games_list(request):
    
    games = (
        Game.objects
        .filter(is_active=True)
        .prefetch_related("genres")
    )
    
    genres = Genre.objects.all()
    
    query = request.GET.get("q", "").strip()
    
    selected_genres = request.GET.getlist("genre")
    selected_platforms = request.GET.getlist("platform")
    selected_statuses = request.GET.getlist("status")
    selected_order = request.GET.get("order", "recent")
    
    
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
        
    if selected_order == "recent":

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

    return render(request, "games/games_detail.html", {
        "game": game,
        "is_in_library": is_in_library,
    })

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
        "games/my_library.html",
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