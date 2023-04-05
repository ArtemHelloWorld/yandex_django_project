import django.contrib.admin

import dishes.models


@django.contrib.admin.register(dishes.models.Ingredient)
class IngredientAdmin(django.contrib.admin.ModelAdmin):
    list_display = (dishes.models.Ingredient.name.field.name,)

    list_display_links = (dishes.models.Ingredient.name.field.name,)


@django.contrib.admin.register(dishes.models.QuantityType)
class QuantityTypeAdmin(django.contrib.admin.ModelAdmin):
    list_display = (dishes.models.QuantityType.name.field.name,)

    list_display_links = (dishes.models.QuantityType.name.field.name,)


@django.contrib.admin.register(dishes.models.IngredientsInstance)
class IngredientsInstanceAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        dishes.models.IngredientsInstance.ingredient.field.name,
        dishes.models.IngredientsInstance.quantity.field.name,
        dishes.models.IngredientsInstance.quantity_type.field.name,
    )

    list_display_links = (
        dishes.models.IngredientsInstance.ingredient.field.name,
    )


@django.contrib.admin.register(dishes.models.DishType)
class DishTypeAdmin(django.contrib.admin.ModelAdmin):
    list_display = (dishes.models.DishType.name.field.name,)

    list_display_links = (dishes.models.DishType.name.field.name,)


@django.contrib.admin.register(dishes.models.Dish)
class DishAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        dishes.models.Dish.name.field.name,
        dishes.models.Dish.type.field.name,
        dishes.models.Dish.complexity.field.name,
        dishes.models.Dish.date_created.field.name,
        dishes.models.Dish.date_updated.field.name,
    )

    list_display_links = (dishes.models.Dish.name.field.name,)

    filter_horizontal = (dishes.models.Dish.ingredients.field.name,)
