from django.http import HttpResponse
from django.views import View
from relatepost.forms import RatingForm
from relatepost.models import Rating


# Когда придёт пост запрос, мы передадим request.POST и получим нашу форму RatingForm,
# Далее проверим форму на валидность, и если форма валидна,
# обновим запись в бд или создадим новую запись если ещё не было записи

# Добавление рейтинга к Посту
class AddStarRating(View):
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user_rate=request.user,
                post_rate_id=int(request.POST.get('car')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
