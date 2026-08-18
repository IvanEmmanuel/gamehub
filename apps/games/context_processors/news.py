from apps.games.models.news import News


def latest_news(request):

    news = (
        News.objects
        .filter(is_published=True)
        .select_related("game")
        .order_by("-published_at")[:3]
    )

    return {
        "latest_news": news,
    }