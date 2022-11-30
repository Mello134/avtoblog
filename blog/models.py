from django.db import models


class Car(models.Model):
    # Id прописывать не нужно - Model Это делает автоматически
    title = models.CharField(max_length=255, verbose_name='Заголовок')  # длина 255 символов
    # unique=True - поле уникально, db_index=True - индексируемое (для ускорения поиска, verbose_name - отображение в адм.)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст статьи')  # текстовое поле без ограничений, blank=True - поле может быть пустым
    tth = models.TextField(blank=True, verbose_name='Технические характеристики авто')
    photo = models.ImageField(upload_to='photos/%Y/%m', verbose_name='Фото')  # загружать будем в photos/год/месяц
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_publisher = models.BooleanField(default=True, verbose_name='Публикация')  # default=True
    # cat_id - id добавится автоматом, ForeignKey - связь Car - c Category
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категории')


class Category(models.Model):
    # db_index - для того чтобы поле было индексированным, поиск по небу будет происходить быстрей
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')