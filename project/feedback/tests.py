import django.test
import django.urls
import feedback.forms
import feedback.models


class FeedbackFormTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_view_item_list(self):
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        self.assertIn('form', response.context)

    def test_labels(self):
        text_help_text = FeedbackFormTests.form.fields['text'].label
        self.assertEqual(text_help_text, 'Ваше сообщение')

        mail_help_text = self.form.fields['mail'].label
        self.assertEqual(mail_help_text, 'Ваша почта')

    def test_create_feedback(self):
        feedback_item_count = feedback.models.Feedback.objects.count()
        form_data = {
            'text': 'Всё замечательно!',
            'mail': '123@yandex.ru'
        }

        response = django.test.Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data
        )

        self.assertRedirects(
            response,
            django.urls.reverse('feedback:feedback')
        )
        self.assertEqual(feedback.models.Feedback.objects.count(),
                         feedback_item_count + 1)
