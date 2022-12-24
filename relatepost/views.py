from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

from blog.models import Car
from relatepost.forms import RatingForm
from relatepost.models import Rating, LikeMarkPost


# Когда придёт пост запрос, мы передадим request.POST и получим нашу форму RatingForm,
# Далее проверим форму на валидность, и если форма валидна,
# обновим запись в бд или создадим новую запись если ещё не было записи

# Добавление рейтинга к Посту (для JS hoogan ajax)
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


# кнопка лайка
@login_required
def like_post(request, cat_slug, car_slug):
    try:
        like_mark_post_object = LikeMarkPost.objects.get(user_like_mark__pk=request.user.pk,
                                                         post_like_mark__slug=car_slug)
        # то же самое что [if like_mark_post_object.is_like_post == False:]
        if not like_mark_post_object.is_like_post:  # если в реакции ЛАЙК = False
            # !update не работает с get! - работает только c filter!
            # меняем лайн на True
            LikeMarkPost.objects.filter(user_like_mark__pk=request.user.pk,
                                        post_like_mark__slug=car_slug).update(is_like_post=True)

        else:  # если в реакции ЛАЙК = True
            # меняем лайн на False
            LikeMarkPost.objects.filter(user_like_mark__pk=request.user.pk,
                                        post_like_mark__slug=car_slug).update(is_like_post=False)
    except LikeMarkPost.DoesNotExist:  # Реакцию не нашли (объект не существует)
        # создаём новую реакцию
        like_mark_post_object = LikeMarkPost.objects.create(
            user_like_mark=request.user,
            post_like_mark=Car.objects.get(slug=car_slug),
            is_like_post=True,
            is_bookmarks_post=False
        )
        like_mark_post_object.save()
    return redirect('car', cat_slug, car_slug)

