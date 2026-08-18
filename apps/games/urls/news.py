from django.urls import path

from ..views.news import news_list, news_detail


app_name = "news"


urlpatterns = [
    path("", news_list, name="news_list"),
    path("<slug:slug>/", news_detail, name="news_detail"),
]