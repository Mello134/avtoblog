from django.contrib import admin
from video.models import VideoYouTubeRuTube, CommentVideoYtRt, LikeMarkVideo


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


# модель лайков и закладок к видео (в админке)
class LikeMarkVideoAdmin(admin.ModelAdmin):
    # отображаемые поля в таблице админки
    list_display = ('user_lm_video', 'video_lm', 'is_like_video', 'is_bookmarks_video')
    # поля по которым можно вести поиск
    search_fields = ('user_lm_video', 'video_lm')
    # редактирование в таблице всех реакций (не заходя в конкретную запись)
    list_editable = ('is_like_video', 'is_bookmarks_video')
    # фильтр по полям
    list_filter = ('user_lm_video', 'video_lm')


# Register your models here.
admin.site.register(VideoYouTubeRuTube, VideoYouTubeRuTubeAdmin)
admin.site.register(CommentVideoYtRt, CommentVideoYtRtAdmin)
admin.site.register(LikeMarkVideo, LikeMarkVideoAdmin)
