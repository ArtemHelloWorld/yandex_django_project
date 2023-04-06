import django.forms

import core.forms
import dishes.models


class NewDishesForm(
    core.forms.BootstrapClassAndPlaceholderFormMixin, django.forms.ModelForm
):
    class Meta:
        model = dishes.models.Dish
        fields = (
            'name',
            'type',
            'ingredients',
            'recipe',
            'complexity',
            'cooking_time',
        )
