from django.db import models

from .game import Game


class News(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    content = models.TextField()
    source_name = models.CharField(max_length=150, blank=True)
    source_url = models.URLField(blank=True)
    # Autor de la noticia original
    author = models.CharField(max_length=150, blank=True)

    image = models.ImageField(
        upload_to="news/",
        blank=True,
        null=True
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news"
    )

    published_at = models.DateTimeField()

    is_published = models.BooleanField(
        default=False
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title