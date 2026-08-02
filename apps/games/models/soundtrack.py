from django.db import models
from urllib.parse import urlparse

from .game import Game


class Soundtrack(models.Model):

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="soundtracks"
    )

    title = models.CharField(max_length=200)

    artist = models.CharField(
        max_length=150,
        blank=True
    )

    spotify_url = models.URLField(
        blank=True
    )

    youtube_url = models.URLField(
        blank=True
    )

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "id"]

    def save(self, *args, **kwargs):

        if not self.pk and self.display_order == 0:

            last_order = (
                Soundtrack.objects
                .filter(game=self.game)
                .aggregate(models.Max("display_order"))
                .get("display_order__max")
            )

            self.display_order = (last_order or 0) + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.game.name} - {self.title}"
    
    
    @property
    def spotify_id(self):
        """
        Extrae el ID del recurso de Spotify desde una URL.

        Soporta enlaces como:

        https://open.spotify.com/track/...
        https://open.spotify.com/album/...
        https://open.spotify.com/playlist/...
        """

        if not self.spotify_url:
            return None

        parsed = urlparse(self.spotify_url)

        if parsed.hostname in (
            "open.spotify.com",
            "www.open.spotify.com",
        ):

            parts = parsed.path.strip("/").split("/")

            if len(parts) >= 2:
                return {
                    "type": parts[0],
                    "id": parts[1]
                }

        return None


    @property
    def embed_url(self):

        if not self.spotify_id:
            return ""

        return (
            f"https://open.spotify.com/embed/"
            f"{self.spotify_id['type']}/"
            f"{self.spotify_id['id']}"
        )
        
    @property
    def spotify_type(self):

        if not self.spotify_id:
            return ""

        return self.spotify_id["type"]