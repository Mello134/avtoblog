# Generated by Django 4.1.3 on 2022-12-17 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relatepost', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercarrelation',
            options={'verbose_name': 'Отношение пользователя к посту', 'verbose_name_plural': 'Отношения пользователей к постам'},
        ),
    ]
