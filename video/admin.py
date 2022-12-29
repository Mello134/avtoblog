from django.contrib import admin
from video.models import VideoYouTubeRuTube, CommentVideoYtRt


# модель видео (в админке)
class VideoYouTubeRuTubeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author_video', 'video_url')
    # список полей - ко которым можно вести поиск
    search_fields = ('name', 'author_video')
    # редактирование поля публикации - в списке - в админке
    list_editable = ('name', 'author_video', 'video_url')  # запятая - если 1 поле!
    # фильтр по полям - публикация, время изменения.
    list_filter = ('author_video',)


# модель комментариев к видео (в админке)
class CommentVideoYtRtAdmin(admin.ModelAdmin):
    list_display = ('pk', 'video', 'author_comment', 'text_comment', 'status_comment')


# Register your models here.
admin.site.register(VideoYouTubeRuTube, VideoYouTubeRuTubeAdmin)
admin.site.register(CommentVideoYtRt, CommentVideoYtRtAdmin)
