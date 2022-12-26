from django.contrib import admin
from video.models import VideoYT


class VideoYTAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author_video', 'video_url')
    # список полей - ко которым можно вести поиск
    search_fields = ('name', 'author_video')
    # редактирование поля публикации - в списке - в админке
    list_editable = ('name', 'author_video', 'video_url')  # запятая - если 1 поле!
    # фильтр по полям - публикация, время изменения.
    list_filter = ('author_video',)


# Register your models here.
admin.site.register(VideoYT, VideoYTAdmin)
