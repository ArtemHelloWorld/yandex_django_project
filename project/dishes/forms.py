import django.forms
import django.db.models

import core.forms
import dishes.models


class NewDishForm(
    core.forms.BootstrapClassAndPlaceholderFormMixin,
    django.forms.ModelForm
):
    class Meta:
        model = dishes.models.Dish
        fields = (
            dishes.models.Dish.name.field.name,
            dishes.models.Dish.type.field.name,
            dishes.models.Dish.recipe.field.name,
            dishes.models.Dish.complexity.field.name,
            dishes.models.Dish.cooking_time.field.name,
        )


class IngredientForm(
    core.forms.BootstrapClassAndPlaceholderFormMixin,
    django.forms.ModelForm
):
    class Meta:
        model = dishes.models.IngredientInstance
        fields = (
            dishes.models.IngredientInstance.ingredient.field.name,
            dishes.models.IngredientInstance.quantity.field.name,
            dishes.models.IngredientInstance.quantity_type.field.name,
        )


IngredientFormSet = django.forms.inlineformset_factory(
    dishes.models.Dish,
    dishes.models.IngredientInstance,
    form=IngredientForm,
    extra=5
)
