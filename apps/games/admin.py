from django.contrib import admin
from .models import (Game, Genre, Achievement, Trailer, Screenshot, DLC, Guide, Soundtrack, PatchNote)
from django.utils.html import format_html

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    search_fields = ('name',)
    
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "developer",
        "publisher",
        "release_date",
        "is_active",
    )
    list_filter = (
        "is_active",
        "release_date",
        "created_at",
    )
    search_fields = ['name', 'overview']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20



@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):

    list_display = (
        "icon_preview",
        "title",
        "game",
        "is_hidden",
        "display_order",
        "hidden",
    )

    list_filter = (
        "is_hidden",
        "game",
    )

    search_fields = (
        "title",
        "description",
        "game__name",
    )

    ordering = (
        "game",
        "display_order",
    )

    list_select_related = (
        "game",
    )

    fieldsets = (

        ("Información general", {
            "fields": (
                "game",
                "title",
            )
        }),

        ("Contenido", {
            "fields": (
                "description",
                "icon",
            )
        }),

        ("Configuración", {
            "fields": (
                "is_hidden",
                "display_order",
            )
        }),

    )
    
    @admin.display(description="Hidden", boolean=True)
    def hidden(self, obj):
        return obj.is_hidden

    @admin.display(description="Icon")
    def icon_preview(self, obj):

        if obj.icon:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:8px; object-fit:cover;">',
                obj.icon.url
            )

        return "-"


@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "game",
        "is_official",
        "display_order",
    )

    list_filter = (
        "is_official",
    )

    search_fields = (
        "title",
        "game__name",
    )

    ordering = (
        "game",
        "display_order",
    )
    
@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "game",
        "display_order",
        "created_at",
    )

    list_filter = (
        "game",
    )

    search_fields = (
        "title",
        "game__name",
    )

    ordering = (
        "game",
        "display_order",
    )


@admin.register(DLC)
class DLCAdmin(admin.ModelAdmin):

    list_display = (
        "cover_preview",
        "title",
        "game",
        "type",
        "release_date",
        "display_order",
    )

    list_filter = (
        "type",
        "game",
    )

    search_fields = (
        "title",
        "game__name",
    )

    ordering = (
        "game",
        "display_order",
    )
    
    @admin.display(description="Cover")
    def cover_preview(self, obj):

        if obj.cover:

            return format_html(
                '<img src="{}" width="60" style="border-radius:6px;">',
                obj.cover.url
            )

        return "-"
    
    fieldsets = (

        ("Información general", {
            "fields": (
                "game",
                "title",
                "type",
            )
        }),

        ("Contenido", {
            "fields": (
                "description",
                "cover",
            )
        }),

        ("Enlaces", {
            "fields": (
                "purchase_url",
            )
        }),

        ("Lanzamiento", {
            "fields": (
                "release_date",
            )
        }),

    )
    
@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):

    list_display = (

        "title",
        "game",
        "source",
        "open_guide",
        "display_order",

    )

    list_filter = (
        "source",
        "game",
    )

    search_fields = (
        "title",
        "description",
        "game__name",
    )

    ordering = (
        "game",
        "display_order",
    )
    
    @admin.display(description="URL")
    def open_guide(self, obj):

        return format_html(
            '<a href="{}" target="_blank">🔗 Abrir</a>',
            obj.url
        )

    fieldsets = (

        ("Información general", {
            "fields": (
                "game",
                "title",
                "source",
            )
        }),

        ("Contenido", {
            "fields": (
                "description",
            )
        }),

        ("Enlace", {
            "fields": (
                "url",
            )
        }),

        ("Organización", {
            "fields": (
                "display_order",
            )
        }),

    )
    

@admin.register(Soundtrack)
class SoundtrackAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "artist",
        "game",
        "spotify_link",
        "display_order",
    )

    list_filter = (
        "game",
    )

    search_fields = (
        "title",
        "artist",
        "game__name",
    )

    ordering = (
        "game",
        "display_order",
    )

    list_select_related = (
        "game",
    )

    fieldsets = (

        ("Información general", {
            "fields": (
                "game",
                "title",
                "artist",
            )
        }),

        ("Enlaces", {
            "fields": (
                "spotify_url",
                "youtube_url",
            )
        }),

        ("Configuración", {
            "fields": (
                "display_order",
            )
        }),

    )

    @admin.display(description="Spotify")
    def spotify_link(self, obj):

        if obj.spotify_url:

            icon = {
                "track": "🎵",
                "album": "💿",
                "playlist": "📀",
            }.get(obj.spotify_type, "🔗")

            return format_html(
                '<a href="{}" target="_blank">{} Abrir</a>',
                obj.spotify_url,
                icon,
            )

        return "-"


@admin.register(PatchNote)
class PatchNoteAdmin(admin.ModelAdmin):

    list_display = (
        "version_display",
        "title",
        "game",
        "release_date",
        "display_order",
    )

    list_filter = (
        "game",
        "release_date",
    )

    search_fields = (
        "version",
        "title",
        "description",
        "game__name",
    )

    ordering = (
        "game",
        "display_order",
    )

    list_select_related = (
        "game",
    )

    fieldsets = (

        ("Información general", {
            "fields": (
                "game",
                "version",
                "title",
            )
        }),

        ("Contenido", {
            "fields": (
                "description",
            )
        }),

        ("Publicación", {
            "fields": (
                "release_date",
                "official_url",
            )
        }),

        ("Configuración", {
            "fields": (
                "display_order",
            )
        }),

    )
    
    @admin.display(description="Version")
    def version_display(self, obj):
        return f"v{obj.version}"