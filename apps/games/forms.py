from django import forms

from .models import (Game, Genre, Trailer, Screenshot, Achievement, Soundtrack, DLC)


class GameForm(forms.ModelForm):
    
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.order_by("name"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:

        model = Game

        fields = [
            "name",
            "slug",
            "overview",
            "genres",
            "release_date",
            "pegi",
            "developer",
            "publisher",
            "platforms",
            "has_multiplayer",
            "trailer_url",
            "official_website",
            "cover",
            "banner",
        ]
        
        widgets = {

            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Cyberpunk 2077",
                    "class": "form-control",
                }
            ),

            "slug": forms.TextInput(
                attrs={
                    "placeholder": "🔒",
                    "readonly": True,
                    "class": "form-control",
                }
            ),

            "overview": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Describe el juego...",
                    "class": "form-control",
                }
            ),

            "release_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            
            "has_multiplayer": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            
            "cover": forms.FileInput(
                attrs={
                    "accept": "image/*",
                }
            ),

            "banner": forms.FileInput(
                attrs={
                    "accept": "image/*",
                }
            ),
            
            "trailer_url": forms.URLInput(
                attrs={
                    "placeholder": "https://youtube.com/...",
                    "class": "form-control",
                }
            ),

            "official_website": forms.URLInput(
                attrs={
                    "placeholder": "https://...",
                    "class": "form-control",
                }
            ),
            
            "developer": forms.TextInput(
                attrs={
                    "placeholder": "CD Projekt Red",
                    "class": "form-control",
                }
            ),

            "publisher": forms.TextInput(
                attrs={
                    "placeholder": "CD Projekt",
                    "class": "form-control",
                }
            ),
            "platforms": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "PC, PlayStation 5, Xbox Series X|S",
                    "class": "form-control",
                }
            ),
        }
        
class TrailerForm(forms.ModelForm):

    class Meta:

        model = Trailer

        fields = [
            "title",
            "youtube_url",
            "is_official",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Halo Infinite Official Campaign Trailer",
                    "class": "form-control",
                }
            ),

            "youtube_url": forms.URLInput(
                attrs={
                    "placeholder": "https://www.youtube.com/watch?v=...",
                    "class": "form-control",
                }
            ),

            "is_official": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }
        
class ScreenshotForm(forms.ModelForm):

    class Meta:

        model = Screenshot

        fields = [
            "title",
            "image",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Master Chief en Zeta Halo",
                    "class": "form-control",
                }
            ),

            "image": forms.FileInput(
                attrs={
                    "accept": "image/*",
                }
            ),

        }
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["image"].required = False
        
class AchievementForm(forms.ModelForm):

    class Meta:

        model = Achievement

        fields = [
            "title",
            "description",
            "icon",
            "is_hidden",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Completa la campaña",
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe cómo obtener este logro...",
                    "class": "form-control",
                }
            ),

            "icon": forms.FileInput(
                attrs={
                    "accept": "image/*",
                }
            ),

            "is_hidden": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }

        labels = {
            "title": "Título",
            "description": "Descripción",
            "icon": "Icono",
            "is_hidden": "Logro oculto",
        }
        
class SoundtrackForm(forms.ModelForm):

    class Meta:

        model = Soundtrack

        fields = [
            "title",
            "artist",
            "spotify_url",
            "youtube_url",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Halo Infinite Original Soundtrack",
                    "class": "form-control",
                }
            ),

            "artist": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Gareth Coker",
                    "class": "form-control",
                }
            ),

            "spotify_url": forms.URLInput(
                attrs={
                    "placeholder": "https://open.spotify.com/...",
                    "class": "form-control",
                }
            ),

            "youtube_url": forms.URLInput(
                attrs={
                    "placeholder": "https://www.youtube.com/...",
                    "class": "form-control",
                }
            ),

        }

        labels = {
            "title": "Título",
            "artist": "Artista",
            "spotify_url": "Spotify",
            "youtube_url": "YouTube",
        }
        
class DLCForm(forms.ModelForm):

    class Meta:

        model = DLC

        fields = [
            "title",
            "description",
            "type",
            "cover",
            "release_date",
            "purchase_url",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Ej. Halo Infinite: Campaign Expansion",
                    "class": "form-control",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe el contenido de este DLC...",
                    "class": "form-control",
                }
            ),

            "type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "cover": forms.FileInput(
                attrs={
                    "accept": "image/*",
                    "class": "form-control",
                }
            ),

            "release_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "purchase_url": forms.URLInput(
                attrs={
                    "placeholder": "https://...",
                    "class": "form-control",
                }
            ),

        }

        labels = {
            "title": "Título",
            "description": "Descripción",
            "type": "Tipo",
            "cover": "Portada",
            "release_date": "Fecha de lanzamiento",
            "purchase_url": "Enlace de compra",
        }
        
