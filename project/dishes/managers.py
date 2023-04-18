import django.db.models

import dishes.models


class DishManager(django.db.models.Manager):
    def get_queryset(self):
        return (
            super(DishManager, self)
            .get_queryset()
            .select_related('author')
            .select_related('type')
            .prefetch_related('ingredients')
            .prefetch_related('tags')
        )

    def on_home_page(self):
        return self.get_queryset().filter(
            django.db.models.Q(is_on_home_page=True)
            & django.db.models.Q(moderation_status=dishes.models.Dish.ADDED)
        )

    def active(self):
        return self.get_queryset().filter(
            django.db.models.Q(moderation_status=dishes.models.Dish.ADDED)
        )


class IngredientInstanceManager(django.db.models.Manager):
    def get_queryset(self):
        return (
            super(IngredientInstanceManager, self)
            .get_queryset()
            .select_related('ingredient')
            .select_related('dish')
        )
