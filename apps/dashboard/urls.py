from django.urls import path
from . import views
from apps.profiles.views import ProfileUpdateView,CustomPasswordChangeView


urlpatterns = [
    path("", views.dashboard_home, name="dashboard"),
    path("profile/", ProfileUpdateView.as_view(), name="dashboard_profile"),
    path("settings/password/", CustomPasswordChangeView.as_view(), name="change_password",),
    path("library/", views.dashboard_library, name="dashboard_library"),
]