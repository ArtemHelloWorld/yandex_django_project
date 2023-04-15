import django.conf
import django.contrib
import django.core.mail
import django.shortcuts
import django.urls
import feedback.forms


class FeedbackView(django.views.generic.FormView):
    template_name = 'feedback/feedback.html'
    form_class = feedback.forms.FeedbackForm

    def form_valid(self, form):
        django.core.mail.send_mail(
            'Спасибо за заполнение формы!',
            (
                'Благодарим Вас за отзыв о работе нашего сервиса. '
                f'Содержимое вашего письма - "{form.cleaned_data["text"]}"\n'
                'Скоро мы с Вами свяжемся!'
            ),
            django.conf.settings.EMAIL_HOST_USER,
            [form.cleaned_data['mail']],
            fail_silently=False,
        )

        feedback_item = feedback.models.Feedback.objects.create(
            **form.cleaned_data
        )
        feedback_item.save()
        django.contrib.messages.success(
            self.request, 'Форма отправлена успешно!'
        )
        return django.shortcuts.redirect(
            django.urls.reverse('feedback:feedback'),
        )
