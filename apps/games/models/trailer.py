from urllib.parse import urlparse, parse_qs
from django.db import models
from .game import Game


class Trailer(models.Model):

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="trailers"
    )

    title = models.CharField(max_length=200)

    youtube_url = models.URLField()

    is_official = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "id"]
        
    def save(self, *args, **kwargs):

        if not self.pk and self.display_order == 0:

            last_order = (
                Trailer.objects.filter(game=self.game)
                .aggregate(models.Max("display_order"))
                .get("display_order__max")
            )

            self.display_order = (last_order or 0) + 1

        super().save(*args, **kwargs)

        def __str__(self):
            return f"{self.game.name} - {self.title}"


    @property
    def youtube_id(self):
        """
        Extrae el ID del video desde una URL de YouTube.
        Soporta:
        - https://www.youtube.com/watch?v=...
        - https://youtu.be/...
        """

        parsed = urlparse(self.youtube_url)

        if parsed.hostname == "youtu.be":
            return parsed.path[1:]

        if parsed.hostname in (
            "www.youtube.com",
            "youtube.com",
        ):
            return parse_qs(parsed.query).get("v", [None])[0]

        return None

    @property
    def thumbnail_url(self):

        if not self.youtube_id:
            return ""

        return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"

    @property
    def embed_url(self):

        if not self.youtube_id:
            return ""

        return f"https://www.youtube.com/embed/{self.youtube_id}"