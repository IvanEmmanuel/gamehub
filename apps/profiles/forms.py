from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'np-input',
        })
    )

    first_name = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'np-input',
        })
    )

    last_name = forms.CharField(
        label="Apellido",
        widget=forms.TextInput(attrs={
            'class': 'np-input',
        })
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'gamer_tag', 
            'bio',
            'avatar',
            'banner',
            'website',
            'youtube_url', 
            'twitch_url',
            'discord_username',
            'x_url',
            'instagram_url',
            'facebook_url',
            'tiktok_url',  
            'country',
            'city',
            'favorite_platform',
            'favorite_genre',
            'favorite_game', 
            'favorite_quote',
        ]
        
        widgets = {
            'gamer_tag': forms.TextInput(attrs={
                'class': 'np-input',
            }),

            'bio': forms.Textarea(attrs={
                'class': 'np-textarea',
                'rows': 5,
            }),

            'city': forms.TextInput(attrs={
                'class': 'np-input',
            }),

            'country': forms.TextInput(attrs={
                'class': 'np-input',
            }),

            'website': forms.URLInput(attrs={
                'class': 'np-input',
            }),

            'youtube_url': forms.URLInput(attrs={
                'class': 'np-input',
            }),

            'twitch_url': forms.URLInput(attrs={
                'class': 'np-input',
            }),

            'x_url': forms.URLInput(attrs={
                'class': 'np-input',
            }),

            'instagram_url': forms.URLInput(attrs={
                'class': 'np-input',
            }),

            'facebook_url': forms.URLInput(attrs={
                'class': 'np-input',
            }),

            'tiktok_url': forms.URLInput(attrs={
                'class': 'np-input',
            }),

            'discord_username': forms.TextInput(attrs={
                'class': 'np-input',
            }),
            
            'favorite_platform': forms.TextInput(attrs={
                'class': 'np-input',
            }),

            'favorite_genre': forms.TextInput(attrs={
                'class': 'np-input',
            }),

            'favorite_game': forms.TextInput(attrs={
                'class': 'np-input',
            }),

            'favorite_quote': forms.Textarea(attrs={
                'class': 'np-textarea',
                'rows': 3,
            })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        if self.instance.gamer_tag:
            self.fields['gamer_tag'].disabled = True
        
        if user:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            
    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.instance.user
        
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            profile.save()
            
        return profile
          
          
class CustomRegisterForm(UserCreationForm):
    first_name =  forms.CharField(max_length=30, required=True, label='Nombre')
    last_name =  forms.CharField(max_length=30, required=True, label='Apellido')
    email =  forms.EmailField(required=True, label='Correo electronico')
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya esta registrado")
        return email

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "class": "form-control auth-input",
                "placeholder": "Ingresa tu usuario",
                "autocomplete": "username",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control auth-input",
                "placeholder": "Ingresa tu contraseña",
                "autocomplete": "current-password",
            }
        ),
    )