from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField  # django-embed-video


# Видеофайлы YouTube/Rutube
class VideoYouTubeRuTube(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название видео')
    video_url = models.URLField(verbose_name='Ссылка на видео')  # ссылка стороннего видео - django-embed-video
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    author_video = models.ForeignKey(User, on_delete=models.SET_DEFAULT, verbose_name='Автор', default=1, blank=False)

    def __str__(self):
        return f'Видео: {self.name}, Автор видео: {self.author_video}'

    class Meta:
        verbose_name = "Видеофайл c YouTube/RuTube"
        verbose_name_plural = "Видеофайл c YouTube/RuTube"
        ordering = ['-time_update']

    # метод будет автоматически конвертировать ссылку, для возможности отображения у себя на сайте
    # Это политика YouTube/RuTube
    # по сути берём ссылку пользователя, и конвертируем в ссылку для разработчика!
    def safe_url(self):
        url = str(self.video_url)  # получаю обычный url
        if 'youtu.be' in url:
            final_url = url[:8] + 'www.youtube.com/embed' + url[16:]
        elif 'rutube.ru/video' in url:
            final_url = url[:18] + 'play/embed' + url[23:]
        else:
            final_url = url
        return final_url
