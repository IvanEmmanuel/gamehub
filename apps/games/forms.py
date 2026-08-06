from django import forms

from .models import Game, Genre


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