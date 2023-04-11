import django.forms

from . import models


class BootstrapForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class FeedbackForm(BootstrapForm):
    class Meta:
        model = models.Feedback
        fields = (
            models.Feedback.text.field.name,
            models.Feedback.mail.field.name,
        )
        labels = {
            models.Feedback.text.field.name: "Сообщение",
            models.Feedback.mail.field.name: "Ваша электронная почта",
        }
        help_texts = {
            models.Feedback.text.field.name: "Введите своё обращение",
            models.Feedback.mail.field.name: "Введите свою электронную почту",
        }
