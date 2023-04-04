import django.contrib.auth.models
import django.db.models

import users.managers


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
        null=False,
        blank=False,
    )

    birthday = django.db.models.DateField(
        null=True, blank=True, verbose_name='дата рождения'
    )

    image = django.db.models.ImageField(
        upload_to='item/main/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='аватарка',
    )

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профиль'


class User(django.contrib.auth.models.User):
    objects = users.managers.MyUserManager()

    class Meta:
        proxy = True
