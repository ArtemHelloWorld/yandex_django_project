import django.urls
import feedback.forms
import feedback.views

app_name = 'feedback'

urlpatterns = [
    django.urls.path(
        '',
        feedback.views.FeedbackView.as_view(
            template_name='feedback/feedback.html',
            form_class=feedback.forms.FeedbackForm,
        ),
        name='feedback',
    ),
]
