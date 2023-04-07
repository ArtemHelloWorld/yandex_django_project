import django.contrib.auth.mixins
import django.shortcuts
import django.views.generic

import dishes.forms
import dishes.models


class NewDishesView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.FormView,
):
    template_name = 'dishes/dish_new.html'
    form_class = dishes.forms.NewDishesForm

    def form_valid(self, form):
        dish = form.save(commit=False)

        dish.author = self.request.user
        dish.save()

        return django.shortcuts.redirect('home:home')


class DishDetailView(django.views.generic.DetailView):
    queryset = dishes.models.Dish.objects.prefetch_related('ingredients').all()
    pk_url_kwarg = 'dish_pk'
    template_name = 'dishes/dish_detail.html'
