import django.db.models


class Feedback(django.db.models.Model):
    RECEIVED = 'received'
    HANDLING = 'handling'
    ANSWERED = 'answered'

    STATUS_CHOICES = [
        (RECEIVED, 'Получено'),
        (HANDLING, 'В обработке'),
        (ANSWERED, 'Ответ дан'),
    ]

    text = django.db.models.TextField(
        'текст сообщения',
    )

    personal_information = django.db.models.OneToOneField(
        'PersonalInformation',
        on_delete=django.db.models.CASCADE,
        related_name='personal_information',
        default=0,
    )

    status = django.db.models.CharField(
        choices=STATUS_CHOICES,
        max_length=8,
        default=RECEIVED,
        verbose_name='статус',
    )

    created_on = django.db.models.DateTimeField(
        'дата и время создания',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'фидбек'
        verbose_name_plural = 'фидбеки'


class PersonalInformation(django.db.models.Model):
    mail = django.db.models.EmailField(
        'электронная почта',
    )
