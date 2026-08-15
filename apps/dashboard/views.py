from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.games.models.userGameLibrary import UserGameLibrary

# Create your views here.

@login_required
def dashboard_home(request):
    return render(request, "dashboard/dashboard_home.html")

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