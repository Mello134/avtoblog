from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from blog.models import Car


# класс комментарии
class Comment(models.Model):
    # отношение к определенному посту (записи в Car)
    car_post = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Статья', blank=True, null=True,
                                 related_name='comment_car')
    # автор - связь с моделью User
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True,
                                       null=True)
    # дата создания комментария
    time_create_comment = models.DateTimeField(auto_now_add=True, verbose_name='Время создания комментария')
    # текст комментария
    text_comment = models.TextField(verbose_name='Текст комментария')
    # статус комментария (видно/не видно)
    status_comment = models.BooleanField(verbose_name='Видимость комментария', default=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['time_create_comment']  # сортировка

    # отображение записи по данным
    def __str__(self):
        return f'Авто: {self.car_post}, ' \
               f'Коммент: {self.text_comment}'

    # функция формирования маршрута к ссылке
    def get_absolute_url(self):  # self - ссылка на один экземпляр(строку) таблицы модели
        # reverse('имя пути', kwargs={ Category-slug, Car-slug, Comment-slug}
        return reverse('like_button_comment', kwargs={'cat_slug': self.car_post.cat.slug,
                                                      'car_slug': self.car_post.slug,
                                                      'com_id': self.pk})


# Лайки на Комменты
# Буду считать количество LikeComment.objects.filter(comment=comment.pk)
class LikeComment(models.Model):
    # Связь с пользователем
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Лайкнувший пользователь')
    # Связь с определённым комментарием
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий для лайка',
                                related_name='comment_like')

    class Meta:
        verbose_name = "Лайк комментария"
        verbose_name_plural = "Лайки комментария"
        # db_table = 'LikeComment'  # для названия таблицы в DB

    def __str__(self):
        return f'ЛАЙК_К - {self.comment},' \
               f'Пользователь: {self.user}.'
