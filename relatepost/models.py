from django.contrib.auth.models import User
from django.db import models
from blog.models import Car


# Лайки и закладки к посту
class LikeMarkPost(models.Model):
    # какой пользователь
    user_like_mark = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь Л-З')
    # какой пост
    post_like_mark = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Пост Л-З')
    # лайк на пост
    is_like_post = models.BooleanField(default=False, verbose_name='Лайк поста')
    # добавление в закладки
    is_bookmarks_post = models.BooleanField(default=False, verbose_name='Пост в закладке')

    class Meta:
        verbose_name = 'Лайк/Закладка поста'
        verbose_name_plural = 'Лайки/закладки к посту'

    def __str__(self):
        return f'Пользователь: {self.user_like_mark.username} - Статья: {self.post_like_mark.slug}.'


# Просто звёзды от 1 до 5 (одна звезда 1 запись)
class RatingStar(models.Model):
    value = models.SmallIntegerField(verbose_name='Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звёзды рейтинга'
        ordering = ['-value']


# Рейтинг (конкретный пользователь, конкретная статья)
class Rating(models.Model):
    user_rate = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Оценивающий пользователь')
    post_rate = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Оцениваемый пост')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')

    def __str__(self):
        return f'Звезда: {self.star}, Пост: {self.post_rate}, Юзер: {self.user_rate}'

    class Meta:
        verbose_name = 'Рейтинг пользователя к посту'
        verbose_name_plural = 'Рейтинги пользователей к постам'
