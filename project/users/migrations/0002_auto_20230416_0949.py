# Generated by Django 3.2.16 on 2023-04-16 06:49

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='identity_confirmed',
            field=models.BooleanField(
                default=False, verbose_name='подтверждение личности'
            ),
        ),
    ]
