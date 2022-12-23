from django import forms
from blog.models import *


# форма добавления поста
class CarAddForm(forms.ModelForm):
    class Meta:
        model = Car  # наша модель
        # поля отображаемые в форме
        fields = ['slug', 'title', 'content', 'tth', 'photo', 'cat']
        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-control, col-5'}),
            'title': forms.TextInput(attrs={'class': 'form-control, col-10'}),
            'content': forms.Textarea(attrs={'rows': 6, 'class': 'form-control, col-10'}),
            'tth': forms.Textarea(attrs={'rows': 4, 'class': 'form-control, col-10'}),
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
            'title': forms.TextInput(attrs={'class': 'form-control, col-12'}),
            'content': forms.Textarea(attrs={'rows': 15, 'class': 'form-control, col-12'}),
            'tth': forms.Textarea(attrs={'rows': 10, 'class': 'form-control, col-12'}),
        }


