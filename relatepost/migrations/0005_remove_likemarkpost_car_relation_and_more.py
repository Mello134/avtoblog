# Generated by Django 4.1.3 on 2022-12-23 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0009_remove_car_rating'),
        ('relatepost', '0004_ratingstar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likemarkpost',
            name='car_relation',
        ),
        migrations.RemoveField(
            model_name='likemarkpost',
            name='user_relation',
        ),
        migrations.AddField(
            model_name='likemarkpost',
            name='post_like_mark',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.car', verbose_name='Пост Л-З'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='likemarkpost',
            name='user_like_mark',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь Л-З'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.car', verbose_name='Оцениваемый пост')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='relatepost.ratingstar', verbose_name='Звезда')),
                ('user_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Оценивающий пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг пользователя к посту',
                'verbose_name_plural': 'Рейтинги пользователей к постам',
            },
        ),
    ]
