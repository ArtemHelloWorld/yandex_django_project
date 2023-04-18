import dishes.models


def search_dishes_by_ingredients(user_ingredients):
    dishes_list = dishes.models.Dish.objects.active().filter(
        ingredients__ingredient__in=user_ingredients
    )

    dishes_dict = {}
    for dish in dishes_list:
        necessary_ingredients = dish.ingredients.all()

        dishes_dict[dish] = {
            'necessary_ingredients': necessary_ingredients,
            'missing_ingredients': _get_missing_ingredients(
                necessary_ingredients, user_ingredients
            ),
        }
    return _get_to_buy_dict(dishes_dict)


def _get_missing_ingredients(necessary_ingredients, user_ingredients):
    return [
        ingredient.ingredient
        for ingredient in necessary_ingredients
        if ingredient.ingredient not in user_ingredients
    ]


def _get_to_buy_dict(dishes_dict):
    dishes_dict = dict(
        sorted(
            dishes_dict.items(), key=lambda x: len(x[1]['missing_ingredients'])
        )
    )

    to_buy_dict = {}

    for dish, ingredients in dishes_dict.items():
        len_missing = len(ingredients['missing_ingredients'])
        len_necessary = len(ingredients['necessary_ingredients'])

        persentage_of_missing_products = len_missing / len_necessary

        if len_missing <= 3 and persentage_of_missing_products <= 0.5:
            to_buy_dict[dish] = ingredients['missing_ingredients']

    return to_buy_dict
