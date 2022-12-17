from django.contrib import admin
from relatepost.models import UserCarRelation


class UserCarRelationAdmin(admin.ModelAdmin):
    # список отображаемых столбцов в админ-панели
    list_display = ('id', 'user_relation', 'car_relation', 'is_like_post', 'is_bookmarks_post', 'rate')
    # список полей на которые можно кликнуть - для редактирования
    list_display_links = ('user_relation', 'car_relation')
    # список полей - ко которым можно вести поиск
    search_fields = ('user_relation', 'car_relation')
    # редактирование поля публикации - в списке - в админке
    list_editable = ('is_like_post', 'is_bookmarks_post', 'rate')  # запятая - если 1 поле!
    # фильтр по полям - публикация, время изменения.
    list_filter = ('user_relation', 'car_relation')


# Register your models here.
admin.site.register(UserCarRelation, UserCarRelationAdmin)
