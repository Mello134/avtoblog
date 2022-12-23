from django import forms

from relatepost.models import RatingStar, Rating


# форма изменения и добавления рейтинга к посту
class RatingForm(forms.ModelForm):
    # где empty_label - это чёрточки при выборе(например категорий)
    # RadioSelect - это тыканье на кнопку вместо выпадающего списка (есть чек бокс,
    # queryset - Это все записи, то есть все звёзды 1 2 3 4 5

    # здесь мы переопределяем поле star
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating  # связь с моделью юзер-пост-рейтинг
        fields = ('star',)
