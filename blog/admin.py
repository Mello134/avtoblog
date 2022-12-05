from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class CarAdmin(admin.ModelAdmin):
    # список отображаемых столбцов в админ-панели
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published', 'author')
    prepopulated_fields = {'slug': ('title',)}  # автозаполнение слага по имени поста
    # список полей на которые можно кликнуть - для редактирования
    list_display_links = ('id', 'title')
    # список полей - ко которым можно вести поиск
    search_fields = ('title', 'content')
    # редактирование поля публикации - в списке - в админке
    list_editable = ('is_published', 'author')  # запятая - если 1 поле!
    # фильтр по полям - публикация, время изменения.
    list_filter = ('is_published', 'time_create')

    # отображение миниатюр фото в админке
    def get_html_photo(self, object):
        if object.photo:  # если фото есть
            # mark_safe - не экранирует теги
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # автозаполнение слага по имени категории
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)  # ЗАПЯТАЯ В КОНЦЕ- при одном поле


# Register your models here.
admin.site.register(Car, CarAdmin)
admin.site.register(Category, CategoryAdmin)
