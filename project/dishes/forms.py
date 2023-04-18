import django.core.exceptions
import django.forms

import core.forms
import dishes.models
import dishes.widgets


class NewDishForm(
    core.forms.BootstrapClassFormMixin,
    core.forms.BootstrapPlaceholderFormMixin,
    django.forms.ModelForm,
):
    class Meta:
        model = dishes.models.Dish
        fields = (
            dishes.models.Dish.name.field.name,
            dishes.models.Dish.image_main.field.name,
            dishes.models.Dish.type.field.name,
            'tags',
            dishes.models.Dish.recipe.field.name,
            dishes.models.Dish.complexity.field.name,
            dishes.models.Dish.cooking_time.field.name,
        )

        widgets = {
            dishes.models.Dish.cooking_time.field.name: (
                dishes.widgets.DurationWidget()
                )
        }


class NewIngredientForm(
    core.forms.BootstrapClassFormMixin,
    core.forms.BootstrapPlaceholderFormMixin,
    django.forms.ModelForm,
):
    class Meta:
        model = dishes.models.Ingredient
        fields = (dishes.models.Ingredient.name.field.name,)


class IngredientForm(
    core.forms.BootstrapClassFormMixin,
    core.forms.BootstrapPlaceholderFormMixin,
    django.forms.ModelForm,
):
    class Meta:
        model = dishes.models.IngredientInstance
        fields = (
            dishes.models.IngredientInstance.ingredient.field.name,
            dishes.models.IngredientInstance.quantity.field.name,
            dishes.models.IngredientInstance.quantity_type.field.name,
        )


class IngredientInlineFormSet(django.forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        ingredients = []
        for form in self.forms:
            ingredient = form.cleaned_data.get('ingredient')
            if ingredient in ingredients:
                raise django.core.exceptions.ValidationError(
                    'Ингредиенты в списке не должны повторяться'
                )
            ingredients.append(ingredient)


IngredientFormSet = django.forms.inlineformset_factory(
    dishes.models.Dish,
    dishes.models.IngredientInstance,
    form=IngredientForm,
    formset=IngredientInlineFormSet,
    extra=1,
    can_delete=False,
)


class DishesSearchForm(
    core.forms.BootstrapSelectClassFormMixin,
    django.forms.Form,
):
    ingredient = django.forms.ModelChoiceField(
        queryset=dishes.models.Ingredient.objects.all(),
        empty_label='выберите ингредиент',
    )


DishesSearchFormSet = django.forms.formset_factory(
    form=DishesSearchForm,
    extra=1,
    can_delete=False,
)
