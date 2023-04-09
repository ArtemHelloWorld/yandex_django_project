import django.contrib.auth.mixins
import django.shortcuts
import django.views.generic

import dishes.forms
import dishes.models


class NewDishView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.TemplateView,
):
    template_name = 'dishes/dish_new.html'
    form_class = dishes.forms.NewDishForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        new_dish_form = dishes.forms.NewDishForm()
        ingredient_formset = dishes.forms.IngredientFormSet()

        context['new_dish_form'] = new_dish_form
        context['ingredient_formset'] = ingredient_formset

        return context

    def post(self, request):
        new_dish_form = dishes.forms.NewDishForm(request.POST)
        ingredient_formset = dishes.forms.IngredientFormSet(request.POST)

        if new_dish_form.is_valid() and ingredient_formset.is_valid():
            dish = new_dish_form.save(commit=False)

            dish.author = self.request.user
            dish.save()
            new_dish_form.save_m2m()

            ingredients = ingredient_formset.save(commit=False)

            for ingredient in ingredients:
                ingredient.dish = dish
                ingredient.save()

            return django.shortcuts.redirect('home:home')
        else:
            return django.shortcuts.render(
                request,
                self.template_name,
                {
                    'new_dish_form': new_dish_form,
                    'ingredient_formset': ingredient_formset,
                },
            )


class DishDetailView(django.views.generic.DetailView):
    model = dishes.models.Dish
    pk_url_kwarg = 'dish_pk'
    template_name = 'dishes/dish_detail.html'
