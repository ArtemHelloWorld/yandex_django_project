import django.contrib.auth.mixins
import django.shortcuts
import django.views.generic

import dishes.forms


class NewDishesView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.FormView,
):
    template_name = 'dishes/new_dishes.html'
    form_class = dishes.forms.NewDishesForm

    def form_valid(self, form):
        dish = form.save(commit=False)

        dish.author = self.request.user
        dish.save()

        return django.shortcuts.redirect('home:home')
