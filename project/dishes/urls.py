import django.urls

import dishes.views

app_name = 'dishes'

urlpatterns = [
    django.urls.path(
        'new', dishes.views.NewDishesView.as_view(), name='dish_new'
    ),
    django.urls.path(
        '<int:dish_pk>', dishes.views.DishDetailView.as_view(), name='dish_detail'
    )
]
