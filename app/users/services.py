import datetime

import django.conf
import django.contrib.auth.models
import django.core.mail
import django.core.signing
import django.urls

MESSAGE_REGISTRATION = "Для завершения регистрации перейдите по ссылке:\n{}"
MESSAGE_ACTIVATION_BACK = (
    "Вы превысили максимально количство "
    "попыток входа в аккаунт.\n"
    "Для активации перейдите по ссылке:\n{}"
)


def send_email_with_activation_link(request, user, activation_back=False):
    if activation_back:
        message = MESSAGE_ACTIVATION_BACK.format(
            request.build_absolute_uri(
                generate_activation_link(user, activation_back=True)
            )
        )
    else:
        message = MESSAGE_REGISTRATION.format(
            request.build_absolute_uri(generate_activation_link(user))
        )

    django.core.mail.send_mail(
        subject="Subject",
        message=message,
        from_email=django.conf.settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def generate_activation_link(user, activation_back=False):
    signer = django.core.signing.TimestampSigner()
    if activation_back:
        viewname = "users:back_activate"
    else:
        viewname = "users:signup_activate"

    activation_code = signer.sign(user.username)

    link = django.urls.reverse(
        viewname, kwargs={"activation_code": activation_code}
    )
    return link


def validate_activation_link(value, **kwargs):
    signer = django.core.signing.TimestampSigner()
    max_age = datetime.timedelta(**kwargs)

    try:
        username = signer.unsign(value, max_age=max_age)
    except Exception:
        return None

    user = django.contrib.auth.models.User.objects.get(username=username)
    return user


def generate_normalize_email(email):
    if "@" in email:
        email = email.lower()
        name, domain = email.split("@")

        name = name.split("+")[0]

        if "ya.ru" == domain:
            domain = "yandex.ru"

        if "gmail.com" == domain:
            name = name.replace(".", "")

        if "yandex.ru" == domain:
            name = name.replace(".", "-")

        return f"{name}@{domain}"

    else:
        return email
