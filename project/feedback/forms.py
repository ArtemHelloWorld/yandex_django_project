import django.forms

import core.forms


class FeedbackForm(
    core.forms.BootstrapClassFormMixin,
    core.forms.BootstrapPlaceholderFormMixin,
    django.forms.Form,
):
    text = django.forms.CharField(
        widget=django.forms.Textarea,
        label='Напишите всё, что хотите сказать',
    )
    mail = django.forms.EmailField(
        label='Ваша электронная почта',
    )
