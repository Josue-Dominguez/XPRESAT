from django import forms
from .models import SocialPost, SocialComment

class SocialPostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 dark:bg-dark-third dark:border-dark-third dark:text-dark-txt flex max-w-full sm:text-sm border-gray-300 rounded-md',
            'rows': '3',
            'placeholder': 'Añade una descripcion a tu publicacion'
            }),
        required=True)

    image = forms.FileField(widget=forms.ClearableFileInput(attrs={
        'class': 'relative dark:text-dark-txt dark:bg-dark-second cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500',
        'multiple': True
        }),
        required=False
        )

    class Meta:
        model=SocialPost
        fields=['body']

class SocialCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 dark:bg-dark-third dark:border-dark-third dark:text-dark-txt flex max-w-full sm:text-sm border-gray-300 rounded-md',
            'rows': '1',
            'placeholder': 'Comenta algo...'
            }),
        required=True
        )

    class Meta:
        model=SocialComment
        fields=['comment']        

class ShareForm(forms.Form):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 dark:bg-dark-third dark:border-dark-third dark:text-dark-txt flex max-w-full sm:text-sm border-gray-300 rounded-md',
            'rows': '5',
            'placeholder': 'Añade un comentario a la publicacion que vas a compartir'
            }),
        )
class EncuestaForm(forms.Form):
    OPCIONES = [
        ('si', 'Sí'),
        ('no', 'No'),
        ('no_estoy_seguro', 'No estoy seguro'),
    ]

    pregunta = forms.ChoiceField(
        choices=OPCIONES,
        widget=forms.RadioSelect,
        label="Si soy honesto, prefiero una vida agradable, pacífica, sin grandes dificultades, con suficiente sostén financiero.",
        required=True,
    )