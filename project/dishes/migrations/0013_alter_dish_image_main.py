# Generated by Django 3.2.16 on 2023-04-10 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0012_auto_20230410_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='image_main',
            field=models.ImageField(upload_to='dish/main/%Y/%m/%d', verbose_name='главное фото'),
        ),
    ]
