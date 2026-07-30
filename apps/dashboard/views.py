from django.shortcuts import render

# Create your views here.
def dashboard_home(request):
    return render(request, "dashboard/dashboard_home.html")

def dashboard_profile(request):
    return render(
        request,
        "dashboard/dashboard_profile.html"
    )