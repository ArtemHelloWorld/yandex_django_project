import django.contrib.messages
import django.shortcuts
import django.urls
import django.views.generic

import feedback.forms
import feedback.models
import feedback.services


class FeedbackView(django.views.generic.FormView):
    template_name = 'feedback/feedback.html'
    form_class = feedback.forms.FeedbackForm

    def form_valid(self, form):
        text = form.cleaned_data['text']
        mail = form.cleaned_data['mail']

        feedback.services.send_feedback_mail(text, mail)

        feedback.services.add_feedback_to_db(text, mail)

        django.contrib.messages.success(
            self.request, 'Форма отправлена успешно!'
        )

        return django.shortcuts.redirect(
            django.urls.reverse('feedback:feedback'),
        )
