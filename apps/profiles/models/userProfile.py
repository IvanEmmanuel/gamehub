from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gamer_tag = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )
    #social y websiite
    website = models.URLField(blank=True, null= True)
    youtube_url  = models.URLField(blank=True, null= True)
    twitch_url = models.URLField(blank=True, null= True)
    discord_username = models.CharField(max_length=50,blank=True)
    x_url = models.URLField(blank=True, null= True)
    instagram_url = models.URLField(blank=True, null= True)
    tiktok_url = models.URLField(blank=True, null= True)
    facebook_url = models.URLField(blank=True, null= True)
    
    country = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80, blank=True)
    
    favorite_platform = models.CharField(max_length=50, blank=True)
    favorite_genre = models.CharField(max_length=50, blank=True)
    favorite_game = models.CharField(max_length=100, blank=True)
    favorite_quote = models.CharField(max_length=250, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=150, blank=True)
    
    
    
    def __str__(self):
        return f"Profile of {self.user.username}"