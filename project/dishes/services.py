import dishes.models


def search_dishes_by_ingredients(user_ingredients):
    dishes_list = dishes.models.Dish.objects.filter(
        ingredients__ingredient__in=user_ingredients
    )

    dishes_dict = {}
    for dish in dishes_list:
        dishes_dict[dish] = _get_ingredients_to_buy(dish, user_ingredients)

    return _sort_by_ingredients_similarity(dishes_dict)


def _get_ingredients_to_buy(dish, user_ingredients):
    return [
        ingredient.ingredient
        for ingredient in dish.ingredients.all()
        if ingredient.ingredient not in user_ingredients
    ]


def _sort_by_ingredients_similarity(dishes_dict):
    return dict(sorted(dishes_dict.items(), key=lambda x: len(x[1])))
