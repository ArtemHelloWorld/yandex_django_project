from django.test import TestCase, Client
from django.urls import reverse

from . import forms, models


class FeedbackFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = forms.FeedbackForm()

    def test_view_item_list(self):
        response = Client().get(
            reverse("feedback:feedback")
        )
        self.assertIn("form", response.context)

    def test_labels(self):
        text_label = FeedbackFormTests.form.fields["text"].label
        self.assertEqual(text_label, "Введите Ваше сообщение")

        mail_label = self.form.fields["mail"].label
        self.assertEqual(mail_label, "Введите Вашу почту")

    def test_create_feedback(self):
        feedback_item_count = models.Feedback.objects.count()
        form_data = {
            "text": "Всё замечательно!",
            "mail": "123@yandex.ru"
        }

        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data
        )

        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertEqual(models.Feedback.objects.count(),
                         feedback_item_count + 1)
