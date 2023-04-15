# Generated by Django 3.2.16 on 2023-04-09 19:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dishes', '0007_auto_20230409_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='moderation_status',
            field=models.CharField(
                choices=[
                    ('sent', 'Отправлено модератору'),
                    ('handling', 'В обработке'),
                    ('added', 'Добавлено'),
                    ('rejected', 'Отклонено'),
                ],
                default='sent',
                max_length=8,
                verbose_name='статус модерации',
            ),
        ),
    ]
