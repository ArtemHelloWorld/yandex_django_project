# Generated by Django 3.2.16 on 2023-04-05 22:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('dishes', '0002_alter_dish_cooking_time'), ('dishes', '0003_alter_dish_cooking_time'), ('dishes', '0004_alter_dish_cooking_time')]

    dependencies = [
        ('dishes', '0001_initial_squashed_0006_auto_20230405_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='cooking_time',
            field=models.DurationField(help_text='Время готовки в часах', verbose_name='время готовки'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='cooking_time',
            field=models.DurationField(default='00:30:00', help_text='Время готовки в часах', verbose_name='время готовки'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='cooking_time',
            field=models.DurationField(default=datetime.timedelta(seconds=1800), help_text='Время готовки в часах', verbose_name='время готовки'),
        ),
    ]
