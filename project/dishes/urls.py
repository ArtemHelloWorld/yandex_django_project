import django.urls

import dishes.views

app_name = 'dishes'

urlpatterns = [
    django.urls.path(
        'new', dishes.views.NewDishView.as_view(), name='dish_new'
    ),
    django.urls.path(
        '<int:dish_pk>',
        dishes.views.DishDetailView.as_view(),
        name='dish_detail',
    ),
    django.urls.path(
        'search',
        dishes.views.DishSearchView.as_view(),
        name='dishes_search',
    ),
]
