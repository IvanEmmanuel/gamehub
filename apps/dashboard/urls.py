from django.urls import path
from . import views
from apps.profiles.views import ProfileUpdateView


urlpatterns = [
    path("", views.dashboard_home, name="dashboard"),
    path("profile/", ProfileUpdateView.as_view(), name="dashboard_profile"),
]