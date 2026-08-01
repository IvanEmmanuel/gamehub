from django.db import models
from .game import Game

class DLCType(models.TextChoices):

    EXPANSION = "EXPANSION", "Expansion"

    SEASON_PASS = "SEASON_PASS", "Season Pass"

    COSMETIC = "COSMETIC", "Cosmetic"

    CONTENT_PACK = "CONTENT_PACK", "Content Pack"


class DLC(models.Model):

    game = models.ForeignKey(
        Game,
        related_name="dlcs",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)
    
    type = models.CharField(
        max_length=30,
        choices=DLCType.choices,
        default=DLCType.EXPANSION
    )

    cover = models.ImageField(upload_to="games/dlcs/")

    release_date = models.DateField()

    purchase_url = models.URLField(blank=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["display_order", "id"]
        
    def save(self, *args, **kwargs):

        if not self.pk and self.display_order == 0:

            last_order = (
                DLC.objects
                .filter(game=self.game)
                .aggregate(models.Max("display_order"))
                .get("display_order__max")
            )

            self.display_order = (last_order or 0) + 1

        super().save(*args, **kwargs)
    
        def __str__(self):
            return f"{self.game.name} - {self.title}"