from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from ..models.news import News


def news_list(request):

    news_queryset = (
        News.objects
        .filter(is_published=True)
        .select_related("game")
        .order_by("-published_at")
    )

    paginator = Paginator(
        news_queryset,
        9
    )

    page_number = request.GET.get("page")

    news = paginator.get_page(page_number)

    featured_news = (
        News.objects
        .filter(
            is_published=True,
            is_featured=True,
        )
        .select_related("game")
        .order_by("-published_at")
        .first()
    )

    return render(
        request,
        "games/news/news_list.html",
        {
            "news": news,
            "featured_news": featured_news,
        }
    )


def news_detail(request, slug):

    news = get_object_or_404(
        News.objects.select_related("game"),
        slug=slug,
        is_published=True,
    )

    return render(
        request,
        "games/news/news_detail.html",
        {
            "news": news,
        }
    )