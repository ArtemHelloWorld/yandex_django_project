import django.core.validators
import django.db.models
import django.urls
import django_cleanup.signals
import sorl.thumbnail
import taggit_selectize.managers
import tinymce

import core.models
import dishes.managers
import users.models


class Ingredient(
    core.models.UniqueNameFieldMixin,
    core.models.NormalizedNameFieldMixin,
):
    NOT_VERIFIED = 'not verified'
    VERIFIED = 'verified'

    VERIFIED_STATUS_CHOICES = [
        (NOT_VERIFIED, 'Не проверено'),
        (VERIFIED, 'Проверено'),
    ]

    moderation_status = django.db.models.CharField(
        choices=VERIFIED_STATUS_CHOICES,
        default=NOT_VERIFIED,
        max_length=12,
        verbose_name='статус модерации',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ('name', 'pk')

    def __str__(self):
        return self.name


class DishType(core.models.UniqueNameFieldMixin):
    class Meta:
        verbose_name = 'тип блюда'
        verbose_name_plural = 'типы блюд'

    def __str__(self):
        return self.name


class IngredientInstance(django.db.models.Model):
    objects = dishes.managers.IngredientInstanceManager()

    KILOGRAMS = 'kg'
    GRAM = 'gram'
    LITERS = 'liters'
    MILLILITERS = 'milliliters'
    TABLE_SPOON = 'table spoon'
    TEA_SPOON = 'tea spoon'
    PIECE = 'piece'
    PINCH = 'pinch'

    VOLUME_TYPE_CHOICES = [
        (KILOGRAMS, 'килограмм'),
        (GRAM, 'грамм'),
        (LITERS, 'литр'),
        (MILLILITERS, 'миллилитр'),
        (TABLE_SPOON, 'столовая ложка'),
        (TEA_SPOON, 'чайная ложка'),
        (PIECE, 'штука'),
        (PINCH, 'щепотка'),
    ]
    dish = django.db.models.ForeignKey(
        'Dish',
        on_delete=django.db.models.CASCADE,
        related_name='ingredients',
    )
    ingredient = django.db.models.ForeignKey(
        Ingredient,
        on_delete=django.db.models.CASCADE,
        verbose_name='название ингредиента',
        help_text='Укажите название ингредиента. Максимум 100 символов',
    )

    quantity = django.db.models.FloatField(
        validators=[django.core.validators.MinValueValidator(0.0)],
        default=None,
        verbose_name='объём ингредиента',
        help_text='Укажите объём ингредиента',
    )

    quantity_type = django.db.models.CharField(
        choices=VOLUME_TYPE_CHOICES,
        max_length=11,
        verbose_name='тип объёма',
        help_text='Укажите тип объёма ингредиента. Максимум 100 символов',
    )

    def __str__(self):
        return self.ingredient.name

    class Meta:
        verbose_name = 'объект ингредиента'
        verbose_name_plural = 'объекты ингредиентов'


class Dish(django.db.models.Model):
    objects = dishes.managers.DishManager()

    SENT = 'sent'
    HANDLING = 'handling'
    ADDED = 'added'
    REJECTED = 'rejected'

    PROCESSING_STATUS_CHOICES = [
        (SENT, 'Отправлено модератору'),
        (HANDLING, 'В обработке'),
        (ADDED, 'Добавлено'),
        (REJECTED, 'Отклонено'),
    ]

    author = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        verbose_name='автор блюда',
    )

    name = django.db.models.CharField(
        max_length=100,
        verbose_name='название',
        help_text='Укажите название блюда. Максимум 100 символов',
    )

    image_main = django.db.models.ImageField(
        upload_to='dish/main/%Y/%m/%d',
        verbose_name='главное фото',
        help_text='Добавьте красивую фотографию блюда',
    )

    type = django.db.models.ForeignKey(
        DishType,
        null=True,
        on_delete=django.db.models.SET_NULL,
        verbose_name='тип блюда',
        help_text='Укажите тип блюда',
    )

    tags = taggit_selectize.managers.TaggableManager(
        verbose_name='теги',
        help_text='добавьте теги(используйте клавишу enter для ввода)',
    )

    recipe = tinymce.HTMLField(
        validators=[
            django.core.validators.MinLengthValidator(
                50,
                'Рецепт слишком маленький. '
                'Пожалуйста, распишите этапы приготовления более подробно.',
            )
        ],
        verbose_name='рецепт',
        help_text='Рецепт по приготовлению',
    )

    complexity = core.models.IntegerRangeField(
        min_value=1,
        max_value=5,
        default=5,
        verbose_name='сложность блюда',
        help_text='Сложность блюда от 1 до 5',
    )

    cooking_time = django.db.models.DurationField(
        verbose_name='время готовки',
        help_text='Время готовки',
    )

    moderation_status = django.db.models.CharField(
        choices=PROCESSING_STATUS_CHOICES,
        default=SENT,
        max_length=8,
        verbose_name='статус модерации',
    )

    is_on_home_page = django.db.models.BooleanField(
        default=False,
        verbose_name='отображать на главной странице',
        help_text='Поставьте галочку, чтобы отобразить на главной странице',
    )

    date_created = django.db.models.DateTimeField(
        auto_now_add=True, verbose_name='дата создания'
    )

    date_updated = django.db.models.DateTimeField(
        auto_now=True, verbose_name='дата последнего изменения'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return django.urls.reverse(
            'dishes:dish_detail', kwargs={'dish_pk': self.pk}
        )

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'
        ordering = ['-date_created']


def sorl_delete(**kwargs):
    sorl.thumbnail.delete(kwargs['file'])


django_cleanup.signals.cleanup_pre_delete.connect(sorl_delete)
