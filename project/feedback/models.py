import django.db.models


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        'текст',
    )
    mail = django.db.models.EmailField(
        'электронная почта',
    )

    class Meta:
        verbose_name = 'фидбек'
        verbose_name_plural = 'фидбеки'
