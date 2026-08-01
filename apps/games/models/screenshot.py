from django.db import models
from .game import Game

class Screenshot(models.Model):

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="screenshots"
    )

    title = models.CharField(
        max_length=200,
        blank=True
    )

    image = models.ImageField(
        upload_to="games/screenshots/"
    )

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["display_order", "id"]
        
    def save(self, *args, **kwargs):

        if not self.pk and self.display_order == 0:

            last_order = (
                Screenshot.objects
                .filter(game=self.game)
                .aggregate(models.Max("display_order"))
                .get("display_order__max")
            )

            self.display_order = (last_order or 0) + 1

        super().save(*args, **kwargs)
    
        def __str__(self):
            return f"{self.game.name} - {self.title or 'Screenshot'}"