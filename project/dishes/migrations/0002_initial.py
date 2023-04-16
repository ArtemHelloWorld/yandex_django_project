# Generated by Django 3.2.16 on 2023-04-16 05:51

import django.db.models.deletion
import taggit_selectize.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('dishes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='автор блюда',
            ),
        ),
        migrations.AddField(
            model_name='dish',
            name='tags',
            field=taggit_selectize.managers.TaggableManager(
                help_text='добавьте теги(используйте клавишу enter для ввода)',
                through='taggit.TaggedItem',
                to='taggit.Tag',
                verbose_name='теги',
            ),
        ),
        migrations.AddField(
            model_name='dish',
            name='type',
            field=models.ForeignKey(
                help_text='Укажите тип блюда',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='dishes.dishtype',
                verbose_name='тип блюда',
            ),
        ),
    ]
