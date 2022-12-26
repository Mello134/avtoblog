# Generated by Django 4.1.3 on 2022-12-26 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoYouTubeRuTube',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название видео')),
                ('video_url', models.URLField(verbose_name='Ссылка на видео')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('author_video', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Видеофайл',
                'verbose_name_plural': 'Видеофайлы',
                'ordering': ['-time_update'],
            },
        ),
        migrations.DeleteModel(
            name='VideoYT',
        ),
    ]