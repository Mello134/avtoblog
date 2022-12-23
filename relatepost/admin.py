from django.contrib import admin
from relatepost.models import LikeMarkPost, RatingStar, Rating


# лайки закладки в админке
class LikeMarkPostAdmin(admin.ModelAdmin):
    # список отображаемых столбцов в админ-панели
    list_display = ('id', 'user_like_mark', 'post_like_mark', 'is_like_post', 'is_bookmarks_post')
    # список полей на которые можно кликнуть - для редактирования
    list_display_links = ('user_like_mark', 'post_like_mark')
    # список полей - ко которым можно вести поиск
    search_fields = ('user_like_mark', 'post_like_mark')
    # редактирование поля публикации - в списке - в админке
    list_editable = ('is_like_post', 'is_bookmarks_post')  # запятая - если 1 поле!
    # фильтр по полям - публикация, время изменения.
    list_filter = ('user_like_mark', 'post_like_mark')


# просто звёзды в админке
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')


# Рейтинг в админке (конкретный пользователь, конкретная статья)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_rate', 'post_rate', 'star')
    list_display_links = ('user_rate', 'post_rate')
    search_fields = ('user_rate', 'post_rate')
    list_editable = ('star',)  # запятая - если 1 поле!
    list_filter = ('star',)


# Register your models here.
admin.site.register(LikeMarkPost, LikeMarkPostAdmin)
admin.site.register(RatingStar, RatingStarAdmin)
admin.site.register(Rating, RatingAdmin)
