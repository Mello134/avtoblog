# Generated by Django 4.1.3 on 2022-12-23 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_car_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='rating',
        ),
    ]
