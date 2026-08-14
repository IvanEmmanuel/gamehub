
from django import forms

class SupportForm(forms.Form):

    subject = forms.CharField(
        label="Asunto",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "support-input",
                "placeholder": "¿En qué podemos ayudarte?"
            }
        )
    )

    message = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(
            attrs={
                "class": "support-textarea",
                "rows": 7,
                "placeholder": "Cuéntanos detalladamente qué problema estás teniendo..."
            }
        )
    )