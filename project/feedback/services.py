import django.conf
import django.core.mail

import feedback.models

FEEDBACK_MAIL_SUBJECT = 'Спасибо за заполнение формы!'
MESSAGE = (
    'Спасибо за ваш отзыв!\n'
    'Мы получили выше обращение '
    'через форму обратной связи '
    'со следующим сообщением:\n'
    '{}\n'
    'В ближайшее время мы рассмотрим '
    'ваше обращение и отправим письмо '
    'с ответом!'
)


def send_feedback_mail(text, mail):
    django.core.mail.send_mail(
        subject=FEEDBACK_MAIL_SUBJECT,
        message=MESSAGE.format(text),
        from_email=django.conf.settings.EMAIL_HOST_USER,
        recipient_list=[mail],
        fail_silently=False,
    )


def add_feedback_to_db(text, mail):
    personal_information = feedback.models.PersonalInformation.objects.create(
        mail=mail
    )

    feedback.models.Feedback.objects.create(
        text=text, personal_information=personal_information
    )
