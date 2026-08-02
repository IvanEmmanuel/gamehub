from django.db import models
from .game import Game

class Achievement(models.Model):
    
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="achievements"
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    
    icon = models.ImageField(
        upload_to="games/icons/",
        blank=True,
        null=True
    )
    
    is_hidden = models.BooleanField(default=False)
    
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ["display_order", "id"]
        unique_together = (
            "game",
            "title",
        )
        
    def save(self, *args, **kwargs):
    
            if not self.pk and self.display_order == 0:
    
                last_order = (
                    Achievement.objects
                    .filter(game=self.game)
                    .aggregate(models.Max("display_order"))
                    .get("display_order__max")
                )
    
                self.display_order = (last_order or 0) + 1
    
            super().save(*args, **kwargs)
            
    def __str__(self):
        return f"{self.game.name} - {self.title}"