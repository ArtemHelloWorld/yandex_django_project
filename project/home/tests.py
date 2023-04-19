import datetime

import django.forms.models
import django.test
import django.urls

import dishes.models
import users.models


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class HomepageTests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = users.models.User.objects.create(
            username='тестовый пользователь', password='123'
        )
        cls.user.save()

        cls.dish_type = dishes.models.DishType.objects.create(
            name='тестовый тип блюда'
        )
        cls.dishe_published = dishes.models.Dish.objects.create(
            author=cls.user,
            name='тестовое блюдо',
            image_main='dish/main/2023/04/18/test_image.jpg',
            type=cls.dish_type,
            recipe='Рецепт' * 50,
            complexity=1,
            cooking_time=datetime.timedelta(minutes=15),
            moderation_status='added',
            is_on_home_page=True,
        )

        cls.dishe_unpublished = dishes.models.Dish.objects.create(
            author=cls.user,
            name='тестовое блюдо не на главной странице',
            image_main='dish/main/2023/04/18/test_image1.jpg',
            type=cls.dish_type,
            recipe='Рецепт' * 50,
            complexity=1,
            cooking_time=datetime.timedelta(minutes=15),
            moderation_status='added',
            is_on_home_page=False,
        )

        cls.dishe_published.clean()
        cls.dishe_published.save()

        cls.dishe_unpublished.clean()
        cls.dishe_unpublished.save()

    def test_homepage_context(self):
        response = self.client.get(django.urls.reverse('home:home'))
        self.assertIn('dishes', response.context)

    def test_homepage_context_length(self):
        response = self.client.get(django.urls.reverse('home:home'))
        items = response.context['dishes']
        self.assertEqual(len(items), 1)
