from django.conf import settings
from django.db import models

from .game import Game


class UserGameLibrary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "game")

    def __str__(self):
        return f"{self.user.username} agregó {self.game.name}"