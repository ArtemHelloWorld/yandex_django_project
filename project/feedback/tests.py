import django.shortcuts
import django.test
import django.urls

import feedback.forms
import feedback.models

@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class FeedbackFormTests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_feedback_context(self):
        response = self.client.get(django.urls.reverse('feedback:feedback'))
        self.assertIn('form', response.context)

    def test_feedback_redirect(self):
        form_data = {'text': 'Всё замечательно!', 'mail': '123@yandex.ru'}
        response = self.client.post(
            django.shortcuts.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, django.shortcuts.reverse('feedback:feedback')
        )

    def test_feedback_creation(self):
        feedback_item_count = feedback.models.Feedback.objects.count()
        form_data = {'text': 'Всё замечательно!', 'mail': '123@yandex.ru'}
        response = self.client.post(
            django.shortcuts.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, django.shortcuts.reverse('feedback:feedback')
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(), feedback_item_count + 1
        )
