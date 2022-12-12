from django import forms
from django.contrib.auth.models import User

from blog.models import *


# форма добавления поста
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


# форма редактирования поста
class CarUpdateForm(forms.ModelForm):
    # Чтобы не отображалось - На данный момент: http:///...
    photo = forms.ImageField(widget=forms.FileInput)
    # photo = forms.ImageField(required=False, widget=forms.FileInput)
    class Meta:
        model = Car  # связываемся с моделью Car
        # поля отображаемые в форме - URL - не указываю!
        # c photo не всё так просто, коряво + обязательно необходимо изменить изображение
        fields = ['title', 'content', 'tth', 'cat', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 6}),
            'tth': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        }


# форма для комментария
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # наша модель
        # поля отображаемые в форме
        fields = ['text_comment']
        widgets = {
            'text_comment': forms.Textarea(attrs={'rows': 1}),
        }
