import django.conf
import django.core.files.uploadedfile
import django.forms.models
import django.shortcuts
import django.test

import dishes.models
import users.models


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class DishNewTests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = users.models.User.objects.create(username='testuser')
        cls.user.set_password('12345')
        cls.user.save()

        cls.dish_type = dishes.models.DishType.objects.create(
            name='тестовый тип блюда'
        )
        cls.dish_type.save()

        cls.ingredient = dishes.models.Ingredient.objects.create(
            name='тестовый ингредиент'
        )
        cls.ingredient.save()

    def test_dish_creation(self):
        feedback_item_count = dishes.models.Dish.objects.count()
        image_path = (
            f'{django.conf.settings.BASE_DIR}/media/dish/test/test_image.jpg'
        )
        image1 = django.core.files.uploadedfile.SimpleUploadedFile(
            name='test_image.jpg',
            content=open(
                image_path,
                'rb',
            ).read(),
            content_type='image/jpeg',
        )
        form_data = {
            'name': 'тестовое блюдо',
            'image_main': image1,
            'type': self.dish_type.pk,
            'tags': 'теги,',
            'recipe': 'рецепт' * 50,
            'complexity': 1,
            'cooking_time_0': 1,
            'cooking_time_1': 10,
            'ingredients-0-ingredient': 1,
            'ingredients-0-quantity': 2,
            'ingredients-0-quantity_type': 'kg',
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
        }
        self.client.login(username='testuser', password='12345')

        self.client.post(
            django.shortcuts.reverse('dishes:dish_new'),
            data=form_data,
            follow=True,
        )

        self.assertEqual(
            dishes.models.Dish.objects.count(), feedback_item_count + 1
        )
