from django import forms
from blog.models import *


class CarAddForm(forms.ModelForm):
    class Meta:
        model = Car  # наша модель
        # поля отображаемые в форме
        fields = ['title', 'slug', 'content', 'tth', 'photo', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),

            'content': forms.Textarea(attrs={'cols': 60, 'rows': 6}),
            'tth': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        }
