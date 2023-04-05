import django.conf
import django.contrib.admin.widgets
import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

import users.models
import users.services


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control form-control-lg'
            field.field.widget.attrs['placeholder'] = field.field.label


class PasswordResetForm(
    BootstrapFormMixin, django.contrib.auth.forms.PasswordResetForm
):
    pass


class SignUpForm(
    BootstrapFormMixin, django.contrib.auth.forms.UserCreationForm
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if django.contrib.auth.models.User.objects.filter(
            username=username
        ).exists():
            raise django.forms.ValidationError('Такое имя уже существует')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        normalized_email = users.services.generate_normalize_email(email)

        if django.contrib.auth.models.User.objects.filter(
            email=normalized_email
        ).exists():
            raise django.forms.ValidationError('Такая почта уже существует')

        return normalized_email

    class Meta:
        model = django.contrib.auth.models.User
        fields = ('username', 'email', 'password1', 'password2')
        required = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(
    BootstrapFormMixin, django.contrib.auth.forms.AuthenticationForm
):
    username = django.forms.CharField(label='Логин или почта', max_length=254)
