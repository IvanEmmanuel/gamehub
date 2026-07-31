from django.db import models
from django.conf import settings
from .game import Game

class Achievement(models.Model):
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    descriptiion = models.CharField(max_length=200)
    
    icon = models.ImageField(
        upload_to="games/icons/",
        blank=True,
        null=True
    )
    
    is_hidden = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            ordering = ['-created_at']
            
    def __str__(self):
        return self.title