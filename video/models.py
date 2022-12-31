from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField  # django-embed-video поле которое проверят именно youtube ссылку, я от этого отошел


# Видеофайлы YouTube/RuTube
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


# лайки + закладки к видео
class LikeMarkVideo(models.Model):
    """ Модель лайк + закладки для видео.
    Поля:
    1)пользователь, совершающий действия; 2)видео над которым совершают действие;
    3)лайк = нет/да; 4)В закладках у пользователя = нет/да."""
    user_lm_video = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    video_lm = models.ForeignKey(VideoYouTubeRuTube, on_delete=models.CASCADE, verbose_name='Видео',
                                 related_name='video_to_lmv')
    is_like_video = models.BooleanField(default=False, verbose_name='Лайк видео')
    is_bookmarks_video = models.BooleanField(default=False, verbose_name='Видео в закладки')

    class Meta:
        verbose_name = 'Лайк/Закладка видео'
        verbose_name_plural = 'Лайки/закладки к видео'

    def __str__(self):
        return f'Пользователь: {self.user_lm_video}, Видео: {self.video_lm}'


# Комментарии для видео
class CommentVideoYtRt(models.Model):
    video = models.ForeignKey(VideoYouTubeRuTube, on_delete=models.CASCADE, verbose_name='Видео',
                              blank=True, null=True, related_name='comment_video')
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария',
                                       blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания комментария')
    text_comment = models.TextField(verbose_name='Текст комментария')
    # видно/не видно
    status_comment = models.BooleanField(verbose_name='Видимость комментария', default=True)

    class Meta:
        verbose_name = 'Комментарий к видео'
        verbose_name_plural = 'Комментарии к видео'
        ordering = ['-time_create']  # сортировка по дате

    # отображение записи при обращении
    def __str__(self):
        return f'PK_Com: {self.pk} __;' \
               f'Видео: {self.video}; ' \
               f'Комментатор: {self.author_comment}.'


# Лайк для комментария к видео
class LikeCommentVideoYtRt(models.Model):
    # лайкнувший пользователь
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Лайкнувший пользователь')
    # Лайкнутый комментарий
    comment = models.ForeignKey(CommentVideoYtRt, on_delete=models.CASCADE, verbose_name='Лайкнутый комментарий')

    class Meta:
        verbose_name = 'Лайк комментария к видео'
        verbose_name_plural = 'Лайки комментариев к видео'
        # db_table = 'Название таблицы в БД'

    def __str__(self):
        return f'Лайк_Ком_Видео - {self.comment},' \
               f'Лайк_Юзер - {self.user}.'
