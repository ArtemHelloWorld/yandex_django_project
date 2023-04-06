import django.urls

import dishes.views

app_name = 'dishes'

urlpatterns = [
    django.urls.path('new', dishes.views.NewDishesView.as_view(), name='new_dishes'),
]
