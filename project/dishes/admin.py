import django.contrib.admin

import dishes.models


@django.contrib.admin.register(dishes.models.Ingredient)
class IngredientAdmin(django.contrib.admin.ModelAdmin):
    list_display = (dishes.models.Ingredient.name.field.name,)

    list_display_links = (dishes.models.Ingredient.name.field.name,)


@django.contrib.admin.register(dishes.models.IngredientInstance)
class IngredientsInstanceAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        dishes.models.IngredientInstance.ingredient.field.name,
        dishes.models.IngredientInstance.quantity.field.name,
        dishes.models.IngredientInstance.quantity_type.field.name,
    )

    list_display_links = (
        dishes.models.IngredientInstance.ingredient.field.name,
    )


@django.contrib.admin.register(dishes.models.DishType)
class DishTypeAdmin(django.contrib.admin.ModelAdmin):
    list_display = (dishes.models.DishType.name.field.name,)

    list_display_links = (dishes.models.DishType.name.field.name,)


class IngredientInstanceInline(django.contrib.admin.StackedInline):
    model = dishes.models.IngredientInstance
    extra = 1


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

    inlines = (IngredientInstanceInline,)
