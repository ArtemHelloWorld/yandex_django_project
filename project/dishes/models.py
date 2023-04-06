import datetime

import django.db.models

import core.models
import users.models


class Ingredient(core.models.NameFieldMixin):
    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name


class QuantityType(core.models.NameFieldMixin):
    class Meta:
        verbose_name = 'граммовка'
        verbose_name_plural = 'граммовки'

    def __str__(self):
        return self.name


class DishType(core.models.NameFieldMixin):
    class Meta:
        verbose_name = 'тип блюда'
        verbose_name_plural = 'типы блюд'

    def __str__(self):
        return self.name


class IngredientsInstance(django.db.models.Model):
    ingredient = django.db.models.ForeignKey(
        Ingredient,
        on_delete=django.db.models.CASCADE,
        verbose_name='название ингредиента',
        help_text='Укажите название ингредиента. Максимум 100 символов',
    )

    quantity = django.db.models.PositiveIntegerField(
        verbose_name='количество ингредиента',
        help_text='Укажите количество',
    )

    quantity_type = django.db.models.ForeignKey(
        QuantityType,
        null=True,
        on_delete=django.db.models.SET_NULL,
        verbose_name='тип граммовки',
        help_text='Укажите тип граммовки ингредиента. Максимум 100 символов',
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
        on_delete=django.db.models.SET_NULL,
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

    ingredients = django.db.models.ManyToManyField(
        IngredientsInstance,
        verbose_name='ингредиенты',
        help_text='Перечислите необходимые ингредиенты',
    )

    recipe = django.db.models.TextField(
        verbose_name='рецепт', help_text='Рецепт по приготовлению'
    )

    complexity = core.models.IntegerRangeField(
        min_value=1,
        max_value=10,
        default=10,
        verbose_name='сложность блюда',
        help_text='Сложность блюда от 1 до 10',
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

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'

    def __str__(self):
        return self.name
