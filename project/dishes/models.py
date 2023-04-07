import datetime

import django.db.models
import django.urls

import core.models
import users.models


class Ingredient(core.models.NameFieldMixin):
    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name


class DishType(core.models.NameFieldMixin):
    class Meta:
        verbose_name = 'тип блюда'
        verbose_name_plural = 'типы блюд'

    def __str__(self):
        return self.name


class IngredientInstance(django.db.models.Model):
    KILOGRAMS = 'kg'
    GRAM = 'gram'
    LITERS = 'liters'
    MILLILITERS = 'milliliters'
    TABLE_SPOON = 'table spoon'
    TEA_SPOON = 'tea spoon'

    VOLUME_TYPE_CHOICES = [
        (KILOGRAMS, 'килограмм'),
        (GRAM, 'грамм'),
        (LITERS, 'литр'),
        (MILLILITERS, 'миллилитр'),
        (TABLE_SPOON, 'столовая ложка'),
        (TEA_SPOON, 'чайная ложка'),

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

    quantity = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name='объём ингредиента',
        help_text='Укажите объём ингредиента',
    )

    quantity_type = django.db.models.CharField(
        choices=VOLUME_TYPE_CHOICES,
        max_length=11,
        verbose_name='тип объёма',
        help_text='Укажите тип объёма ингредиента. Максимум 100 символов',
    )

    class Meta:
        verbose_name = 'объект ингредиента'
        verbose_name_plural = 'объекты ингредиентов'

    def __str__(self):
        return self.ingredient.name


class Dish(django.db.models.Model):
    author = django.db.models.ForeignKey(
        users.models.User,
        null=True,
        on_delete=django.db.models.CASCADE,
        verbose_name='автор блюда',
    )

    name = django.db.models.CharField(
        max_length=100,
        verbose_name='название',
        help_text='Укажите название блюда. Максимум 100 символов',
    )

    type = django.db.models.ForeignKey(
        DishType,
        null=True,
        on_delete=django.db.models.SET_NULL,
        verbose_name='тип блюда',
        help_text='Укажите тип блюда',
    )

    recipe = django.db.models.TextField(
        verbose_name='рецепт', help_text='Рецепт по приготовлению'
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
        default=datetime.timedelta(minutes=30),
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
