from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard_home, name="dashboard"),

    path("profile/", views.dashboard_profile, name="dashboard_profile"),
]