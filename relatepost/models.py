from django.contrib.auth.models import User
from django.db import models
from blog.models import Car


# отношение пользователя к посту
class UserCarRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Совсем плохо'),
        (2, 'Плохо'),
        (3, 'Нормально'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    )

    # какой пользователь
    user_relation = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Оценивающий пользователь')
    # какой пост
    car_relation = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='оцениваемый пост',
                                     related_name='relation_from_user')
    # лайк на пост
    is_like_post = models.BooleanField(default=False, verbose_name='Лайк поста')
    # добавление в закладки
    is_bookmarks_post = models.BooleanField(default=False, verbose_name='Пост в закладке')
    # оценка поста
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True, verbose_name='Личная оценка поста')

    class Meta:
        verbose_name = 'Отношение пользователя к посту'
        verbose_name_plural = 'Отношения пользователей к постам'

    def __str__(self):
        return f'Пользователь: {self.user_relation.username} - Статья: {self.car_relation}, Л_оценка: {self.rate}.'
