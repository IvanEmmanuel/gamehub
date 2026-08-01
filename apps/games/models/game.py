from django.db import models
from django.conf import settings
from .genre import Genre

class Game(models.Model):
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    overview = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genre, related_name="games")
    release_date = models.DateField(null = True,  blank=True)
    pegi = models.CharField(max_length=15, blank=True, null=True) # Cambiar este campo a choices cuando veamos esa característica en Django.
    developer = models.CharField(max_length=100, blank=True) # TODO: Convertir a ManyToManyField cuando exista el modelo Developer.
    platforms = models.TextField(blank=True, null= True) # TODO: Convertir a ManyToManyField cuando exista el modelo Platform.
    status = models.CharField(max_length=50, blank=True, null=True)  # Cambiar este campo a choices cuando veamos esa característica en Django.
    has_multiplayer = models.BooleanField(default=False)
    publisher = models.CharField(max_length=100, null= True) # TODO: Convertir a ManyToManyField cuando exista el modelo publisher.
    trailer_url = models.URLField(blank=True, null= True)
    official_website = models.URLField(blank=True, null= True)
    is_active = models.BooleanField(default=True)
    
    cover = models.ImageField(
        upload_to="games/covers/",
        blank=True,
        null=True
    )
    
    banner = models.ImageField(
        upload_to="games/banners/",
        blank=True,
        null=True
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name