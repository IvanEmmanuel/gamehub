from django.db import models
from django.conf import settings
from .game import Game
from .achievements import Achievement

class UserAchievement(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)
    uunlocked_at = models.DateTimeField(
        blank=True,
        null=True
    )
    
    class Meta:
        unique_together = ('user', 'achievement')
                
    def __str__(self):
        return f"{self.user.username} - {self.achievement}"