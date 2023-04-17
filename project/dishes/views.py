import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import django.views.generic

import dishes.forms
import dishes.models


class NewDishView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.TemplateView,
):
    template_name = 'dishes/dish_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        new_dish_form = dishes.forms.NewDishForm()
        ingredient_formset = dishes.forms.IngredientFormSet()

        context['new_dish_form'] = new_dish_form
        context['ingredient_formset'] = ingredient_formset

        return context

    def post(self, request):
        new_dish_form = dishes.forms.NewDishForm(request.POST, request.FILES)
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


class NewIngredientView(django.views.generic.CreateView):
    form_class = dishes.forms.NewIngredientForm
    template_name = 'dishes/ingredient_new.html'
    success_url = django.urls.reverse_lazy('dishes:dish_new')


class DishDetailView(django.views.generic.DetailView):
    model = dishes.models.Dish
    pk_url_kwarg = 'dish_pk'
    template_name = 'dishes/dish_detail.html'


class DishSearchView(django.views.generic.TemplateView):
    template_name = 'dishes/dishes_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dishes_search_formset = dishes.forms.DishesSearchFormSet()

        context['dishes_search_formset'] = dishes_search_formset

        return context

    def post(self, request):
        dishes_search_formset = dishes.forms.DishesSearchFormSet(request.POST)
        if dishes_search_formset.is_valid():
            ingredients = dishes_search_formset.cleaned_data
            ingredients_list = [
                ingredient.get('ingredient') for ingredient in ingredients
            ]

            ingredient_instance = (
                dishes.models.IngredientInstance.objects.filter(
                    ingredient__in=ingredients_list
                )
            )

            dishes_dict = {}
            for i in ingredient_instance:
                if i.dish in dishes_dict:
                    dishes_dict[i.dish].append(i)
                else:
                    dishes_dict[i.dish] = [i]

            dishes_dict = dict(
                sorted(dishes_dict.items(), key=lambda x: len(x[1]))
            )

            dishes_to_buy = {}
            for dish, ingredients in dishes_dict.items():
                dishes_to_buy[dish] = [
                    item
                    for item in dish.ingredients.all()
                    if item not in ingredients
                ]

            return django.shortcuts.render(
                request,
                self.template_name,
                {
                    'dishes_search_formset': (
                        dishes.forms.DishesSearchFormSet()
                    ),
                    'dishes_dict': dishes_to_buy,
                },
            )
