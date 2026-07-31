from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "gamer_tag",
        "country",
        "city",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "country",
    )

    search_fields = (
        "user__username",
        "gamer_tag",
        "country",
        "city",
    )

    list_select_related = (
        "user",
    )

    list_per_page = 20
    
    fieldsets = (
        (
            "Información básica",
            {
                "fields": (
                    "user",
                    "gamer_tag",
                    "bio",
                    "avatar",
                )
            },
        ),
        (
            "Ubicación",
            {
                "fields": (
                    "country",
                    "city",
                )
            },
        ),
        (
            "Redes sociales",
            {
                "fields": (
                    "website",
                    "youtube_url",
                    "twitch_url",
                    "discord_username",
                    "x_url",
                    "instagram_url",
                    "facebook_url",
                    "tiktok_url",
                )
            },
        ),
        (
            "Preferencias",
            {
                "fields": (
                    "favorite_platform",
                    "favorite_genre",
                    "favorite_game",
                    "favorite_quote",
                )
            },
        ),
        (
            "Estado",
            {
                "fields": (
                    "status",
                )
            },
        ),
    )