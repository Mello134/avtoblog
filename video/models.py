from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField  # django-embed-video


# Сторонние видеофайлы
class VideoYT(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название видео')
    video_url = EmbedVideoField(verbose_name='Ссылка на видео')  # ссылка стороннего видео - django-embed-video
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    author_video = models.ForeignKey(User, on_delete=models.SET_DEFAULT, verbose_name='Автор', default=1, blank=False)

    def __str__(self):
        return f'Видео: {self.name}, Автор видео: {self.author_video}'

    class Meta:
        verbose_name = "Видеофайл"
        verbose_name_plural = "Видеофайлы"
        ordering = ['-time_update']

    # метод будет высчитывать полную сумму товаров в зависимости от цены и количества в корзине
    def safe_url(self):
        # прайс из Product * колво в корзине
        return self.name + '_123'