import django.forms

import core.forms


class FeedbackForm(
    core.forms.BootstrapClassFormMixin,
    core.forms.BootstrapPlaceholderFormMixin,
    django.forms.Form,
):
    text = django.forms.CharField(
        label='Ваше сообщение',
        widget=django.forms.Textarea,
        max_length=1000,
    )
    mail = django.forms.EmailField(
        label='Ваша почта',
    )
