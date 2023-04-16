import django.contrib.auth.models
import django.db.models


class User(django.contrib.auth.models.AbstractUser):
    image = django.db.models.ImageField(
        upload_to='item/main/%Y/%m/%d',
        null=True,
        blank=True,
        verbose_name='аватарка',
    )

    birthday = django.db.models.DateField(
        null=True, blank=True, verbose_name='дата рождения'
    )

    identity_confirmed = django.db.models.BooleanField(
        default=False,
        verbose_name='подтверждение личности'
    )
