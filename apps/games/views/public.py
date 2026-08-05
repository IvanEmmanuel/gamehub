from django.shortcuts import render, get_object_or_404
from ..models.game import Game
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.


def games_list(request):
    
    games = (
        Game.objects
        .filter(is_active=True)
        .prefetch_related("genres")
    )
    query = request.GET.get("q", "").strip()
    
    if query:
        games = games.filter(
            Q(name__icontains=query) |
            Q(developer__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct()
        
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
        'query_string': query_string
    })

def games_detail(request, slug):
    
    game = get_object_or_404(Game, slug=slug)
    
    return render(request, "games/games_detail.html", {
        'game': game
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