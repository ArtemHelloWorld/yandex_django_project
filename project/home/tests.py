import django.forms.models
import django.test
import django.urls


class HomepageTests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_homepage(self):
        response = self.client.get(django.urls.reverse('home:home'))
        self.assertEqual(response.status_code, 200)
