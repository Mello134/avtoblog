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




# form-label
########################################
# VIEWS.PY - class UpdatePostView(UpdateView):
# перенаправление сделать или нет VIEWS.PY - class UpdatePostView(UpdateView):
# FORMS.PY - PHOTO
# update_post.html - ДОБААВЬ ошибки ИЛИ ОНИ И ТАК РАБОТАЮТ..
# update_post.html - <form action="{%  url 'update_post' car_slug=car.slug cat_slug=car.cat.slug %}" method="post" enctype="multipart/form-data">