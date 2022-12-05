from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Car(models.Model):
    # Id прописывать не нужно - Model Это делает автоматически
    title = models.CharField(max_length=255, verbose_name='Заголовок')  # длина 255 символов
    # unique=True - поле уникально, db_index=True - индексируемое (для ускорения поиска, verbose_name - отображение в адм.)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True,
                               verbose_name='Текст статьи')  # текстовое поле без ограничений, blank=True - поле может быть пустым
    tth = models.TextField(blank=True, verbose_name='Характеристики')
    photo = models.ImageField(upload_to='photos/%Y/%m', verbose_name='Фото')  # загружать будем в photos/год/месяц
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')  # default=True
    # cat_id - id добавится автоматом, ForeignKey - связь Car - c Category
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')
    # автор - (связь с моделью User, при удалении автора - статья переходит админу, стандартно автором будет админ,
    # поле автор не может быть пустым)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, verbose_name='Автор', default=1, blank=False)

    # с помощью метода запись нашего класса будет выводиться по её заголовку
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['title']  # рандом сортировка
        # ordering = ['?']  # рандом сортировка
        # ordering = ['-time_create', 'title']  # сортировка, сначала по дате создания, потом по имени

    # функция формирования маршрута к ссылке
    def get_absolute_url(self):  # self - ссылка на один экземпляр(строку) таблицы модели
        # получаем путь('path name=car, 'car/<slug:car_slug>/) = 127/car/supra)
        return reverse('car', kwargs={'cat_slug': self.cat.slug, 'car_slug': self.slug})  # self.slug - атрибут slug


class Category(models.Model):
    # db_index - для того чтобы поле было индексированным, поиск по небу будет происходить быстрей
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    # будем обращаться к категории по полю name
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']  # сортировка, сначала по name

    # функция формирования маршрута к ссылке
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
