from django.contrib import admin
from .models import (Game, UserGameLibrary, Genre, Review, Achievement, UserAchievement, Trailer, Screenshot, DLC, Guide)
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

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'game__name', 'comment')
    list_select_related = ("user", "game")

@admin.register(UserGameLibrary)
class UserGameLibraryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "game",
        "status",
        "is_favorite",
        "added_at",
    )

    list_filter = (
        "status",
        "is_favorite",
    )

    search_fields = (
        "user__username",
        "game__name",
    )

    list_select_related = (
        "user",
        "game",
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "game",
        "is_hidden",
        "created_at",
    )

    list_filter = (
        "is_hidden",
        "game",
    )

    search_fields = (
        "title",
        "game__name",
    )

    list_select_related = (
        "game",
    )

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "achievement",
        "unlocked",
        "unlocked_at",
    )

    list_filter = (
        "unlocked",
    )

    search_fields = (
        "user__username",
        "achievement__title",
    )

    list_select_related = (
        "user",
        "achievement",
    )
    
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