import django.conf
import django.contrib.admin
import django.contrib.auth.forms
import django.contrib.auth.views
import django.urls

import users.forms
import users.views

app_name = 'users'


urlpatterns = [
    django.urls.path(
        'login/',
        django.contrib.auth.views.LoginView.as_view(
            template_name='users/login/login.html',
            form_class=users.forms.CustomAuthenticationForm,
        ),
        name='login',
    ),
    django.urls.path(
        'logout/',
        django.contrib.auth.views.LogoutView.as_view(),
        name='logout',
    ),
    django.urls.path(
        'password_change/',
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name='users/password_change/password_change.html',
            form_class=type(
                'BootstrapPasswordChangeForm',
                (
                    users.forms.BootstrapFormMixin,
                    django.contrib.auth.forms.PasswordChangeForm,
                ),
                {},
            ),
        ),
        name='password_change',
    ),
    django.urls.path(
        'password_change/done/',
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name='users/password_change/password_change_done.html'
        ),
        name='password_change_done',
    ),
    django.urls.path(
        'password_reset/',
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name='users/password_reset/password_reset.html',
            form_class=type(
                'BootstrapPasswordResetForm',
                (
                    users.forms.BootstrapFormMixin,
                    django.contrib.auth.forms.PasswordResetForm,
                ),
                {},
            ),
            from_email=django.conf.settings.DEFAULT_FROM_EMAIL,
        ),
        name='password_reset',
    ),
    django.urls.path(
        'password_reset/done/',
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name='users/password_reset/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    django.urls.path(
        'reset/<uidb64>/<token>/',
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset/password_reset_confirm.html',
            form_class=type(
                'BootstrapSetPasswordForm',
                (
                    users.forms.BootstrapFormMixin,
                    django.contrib.auth.forms.SetPasswordForm,
                ),
                {},
            ),
        ),
        name='password_reset_confirm',
    ),
    django.urls.path(
        'reset/done/',
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    django.urls.path(
        'signup/', users.views.SignupView.as_view(), name='signup'
    ),
    django.urls.path(
        'signup_complete/',
        users.views.SignupCompleteView.as_view(),
        name='signup_complete',
    ),
    django.urls.path(
        'signup/activate/<str:activation_code>',
        users.views.SignupActivateView.as_view(),
        name='signup_activate',
    ),
    django.urls.path(
        'reactivation/<str:activation_code>',
        users.views.ReactivationView.as_view(),
        name='reactivation',
    ),
]
