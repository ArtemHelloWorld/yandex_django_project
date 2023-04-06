import django.forms

import dishes.models
import users.forms


class NewDishesForm(
    users.forms.BootstrapFormMixin,
    django.forms.ModelForm
):
    class Meta:
        model = dishes.models.Dish
        fields = (
            'name',
            'type',
            'ingredients',
            'recipe',
            'complexity',
            'cooking_time'
        )
