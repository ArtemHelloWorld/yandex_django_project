# Generated by Django 3.2.16 on 2023-04-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('feedback', '0002_alter_feedback_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='mail',
            field=models.EmailField(
                max_length=254, verbose_name='электронная почта'
            ),
        ),
    ]
