import django.views.generic

import dishes.models


class HomeView(django.views.generic.ListView):
    template_name = 'home/home.html'
    context_object_name = 'dishes'

    def get_queryset(self):
        return dishes.models.Dish.objects.all()


