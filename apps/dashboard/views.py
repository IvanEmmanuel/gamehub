from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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