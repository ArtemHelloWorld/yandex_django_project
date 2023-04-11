import django.shortcuts
import django.urls
from django.core.mail import send_mail
from django.contrib import messages

from . import forms, models

from project.settings import EMAIL_TO_SEND_MESSAGES


def feedback(request):
    template = 'feedback/feedback.html'
    form = forms.FeedbackForm(request.POST or None)
    context = {
        'form': form,
    }

    if request.method == 'POST' and form.is_valid():
        send_mail(
            'Спасибо за заполнение формы!',
            ('Благодарим Вас за отзыв о работе нашего сервиса. '
             f'Содержимое вашего письма - "{form.cleaned_data["text"]}"'),
            EMAIL_TO_SEND_MESSAGES,
            [form.cleaned_data['mail']],
            fail_silently=False,
        )

        feedback_item = models.Feedback.objects.create(
            **form.cleaned_data
        )
        feedback_item.save()
        messages.success(request, 'Форма отправлена успешно!')
        return django.shortcuts.redirect(
            django.urls.reverse("feedback:feedback"),
        )
    return django.shortcuts.render(request, template, context)
