from django.db import models
from django.conf import settings
from .game import Game

class UserGameLibrary(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="Pendiente")
    is_favorite = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            unique_together = ('user', 'game')
            
    def __str__(self):
        return f"{self.user.username} - {self.game.name}"