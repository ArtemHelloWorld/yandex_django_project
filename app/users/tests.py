import django.conf
import django.contrib.auth.models
import django.core.mail
import django.shortcuts
import django.test
import django.urls
import freezegun
import parameterized

import users.forms
import users.models
import users.services


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class SignUpTests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_signup_incorrect_password(self):
        count = django.contrib.auth.models.User.objects.count()
        form_data = {
            "username": "testusername",
            "email": "testmail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword",
        }
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            count, django.contrib.auth.models.User.objects.count()
        )

    def test_signup_correct_password(self):
        count = django.contrib.auth.models.User.objects.count()
        form_data = {
            "username": "testusername",
            "email": "testmail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            count + 1, django.contrib.auth.models.User.objects.count()
        )

    @django.test.override_settings(ACTIVATE_USERS=True)
    def test_signup_activate_user_true(self):
        form_data = {
            "username": "testusername",
            "email": "testmail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            django.contrib.auth.models.User.objects.get(
                username="testusername"
            ).is_active,
            True,
        )

    @django.test.override_settings(ACTIVATE_USERS=False)
    def test_signup_activate_user_false(self):
        form_data = {
            "username": "testusername",
            "email": "testmail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            django.contrib.auth.models.User.objects.get(
                username="testusername"
            ).is_active,
            False,
        )

    @django.test.override_settings(ACTIVATE_USERS=False)
    def test_signup_activate_user_false_redirect(self):
        form_data = {
            "username": "testusername",
            "email": "testmail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }
        response = self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, django.shortcuts.redirect("users:signup_complete").url
        )

    @django.test.override_settings(ACTIVATE_USERS=False)
    def test_signup_activate_user_false_mail_send(self):
        form_data = {
            "username": "testusername",
            "email": "testmail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(len(django.core.mail.outbox), 1)

    @freezegun.freeze_time("2023-03-19 00:00:01")
    @django.test.override_settings(ACTIVATE_USERS=False)
    def test_signup_activate_user_false_in_time(self):
        form_data = {
            "username": "testusername",
            "email": "testmail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        email_body = django.core.mail.outbox[0].body

        with freezegun.freeze_time("2023-03-19 11:30:00"):
            self.client.get(
                django.urls.reverse(
                    "users:signup_activate",
                    kwargs={"activation_code": email_body.split("/")[-1]},
                )
            )

            self.assertEqual(
                django.contrib.auth.models.User.objects.get(
                    username="testusername"
                ).is_active,
                True,
            )

    @freezegun.freeze_time("2023-03-19 00:00:01")
    @django.test.override_settings(ACTIVATE_USERS=False)
    def test_signup_activate_user_false_out_of_time(self):
        form_data = {
            "username": "testusername",
            "email": "testmail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        email_body = django.core.mail.outbox[0].body

        with freezegun.freeze_time("2023-03-19 12:30:00"):
            self.client.get(
                django.urls.reverse(
                    "users:signup_activate",
                    kwargs={"activation_code": email_body.split("/")[-1]},
                )
            )

            self.assertEqual(
                django.contrib.auth.models.User.objects.get(
                    username="testusername"
                ).is_active,
                False,
            )


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class LoginTests(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def register_user(self):
        form_data_signup = {
            "username": "testusername",
            "email": "testmail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }

        self.user = self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data_signup,
            follow=True,
        )

    def test_login_by_username(self):
        self.register_user()

        form_data_login = {
            "username": "testusername",
            "password": "Testpassword483",
        }

        response = self.client.post(
            django.shortcuts.reverse("users:login"),
            data=form_data_login,
            follow=True,
        )

        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_by_email(self):
        self.register_user()

        form_data_login = {
            "username": "testmail@mail.ru",
            "password": "Testpassword483",
        }

        response = self.client.post(
            django.shortcuts.reverse("users:login"),
            data=form_data_login,
            follow=True,
        )

        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_incorrect_username(self):
        self.register_user()

        form_data = {
            "username": "incorrect",
            "password": "Testpassword483",
        }
        response = self.client.post(
            django.shortcuts.reverse("users:login"),
            data=form_data,
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)

    def test_login_incorrect_email(self):
        self.register_user()

        form_data = {
            "username": "incorrct@mail.ru",
            "password": "Testpassword483",
        }
        response = self.client.post(
            django.shortcuts.reverse("users:login"),
            data=form_data,
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)

    def test_login_incorrect_password(self):
        self.register_user()

        form_data = {
            "username": "testusername",
            "password": "IncorrctPassword",
        }
        response = self.client.post(
            django.shortcuts.reverse("users:login"),
            data=form_data,
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class EmailFieldNormalizationTest(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = users.forms.SignUpForm()

    def signup_user(self, email):
        form_data_signup = {
            "username": "testusername",
            "email": email,
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }

        self.user = self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data_signup,
            follow=True,
        )

    @parameterized.parameterized.expand(
        [
            ("0", "tEsTmAil@mail.ru", "testmail@mail.ru"),
            ("1", "testmail@mail.ru", "tEsTmaIl@mail.ru"),
            ("2", "testmail@ya.ru", "testmail@yandex.ru"),
            ("3", "testmail@yandex.ru", "testmail@ya.ru"),
            ("4", "testmail+testtag@mail.ru", "testmail@mail.ru"),
            ("5", "testmail@mail.ru", "testmail+testtag@mail.ru"),
            ("6", "t.e.s.t.m.a.i.l@gmail.com", "testmail@gmail.com"),
            ("7", "testmail@gmail.com", "t.e.s.t.m.a.i.l@gmail.com"),
            ("8", "t.e.s.t.m.a.i.l@yandex.ru", "t-e-s-t-m-a-i-l@yandex.ru"),
            ("9", "t-e-s-t-m-a-i-l@yandex.ru", "t.e.s.t.m.a.i.l@yandex.ru"),
            ("10", "t.e.s.t.m.a.i.l@ya.ru", "t-e-s-t-m-a-i-l@yandex.ru"),
            ("11", "t-e-s-t-m-a-i-l@yandex.ru", "t.e.s.t.m.a.i.l@ya.ru"),
            (
                "12",
                "T.e.S.t.M.a.I.l+tEsTtag@ya.ru",
                "t-E-s-T-m-A-i-L@yandex.ru",
            ),
            (
                "13",
                "T-e-S-t-M-a-I-l@yandex.ru",
                "t.E.s.T.m.A.i.L+TESTTAG@ya.ru",
            ),
        ]
    )
    def test_email_valid_changes(self, _, email_signup, email_login):
        self.signup_user(email_signup)

        form_data = {
            "username": email_login,
            "password": "Testpassword483",
        }
        response = self.client.post(
            django.shortcuts.reverse("users:login"),
            data=form_data,
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    @parameterized.parameterized.expand(
        [
            ("0", "testmail@mail.ru", "test@mail.ru"),
            ("1", "testmail@mail.ru", "testmail@gmail.com"),
            ("2", "testmail@ya.ru", "testmail@gmail.com"),
            ("3", "t.e.s.t.m.a.i.l@yandex.ru", "testmail@yandex.ru"),
            ("4", "t.e.s.t.m.a.i.l@gmail.com", "t-e-s-t-m-a-i-l@gmail.com"),
            ("5", "testmail@mail.ru", "testmail"),
        ]
    )
    def test_email_invalid_changes(self, _, email_signup, email_login):
        self.signup_user(email_signup)

        form_data = {
            "username": email_login,
            "password": "Testpassword483",
        }
        response = self.client.post(
            django.shortcuts.reverse("users:login"),
            data=form_data,
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class ActivationBackClass(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def registrate_user(self):
        form_data_signup = {
            "username": "testusername",
            "email": "testemail@mail.ru",
            "password1": "Testpassword483",
            "password2": "Testpassword483",
        }

        self.user = self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=form_data_signup,
            follow=True,
        )

    def test_over_login_mail_send(self):
        self.registrate_user()

        mail_counts = len(django.core.mail.outbox)

        form_data_incorrect = {
            "username": "testusername",
            "password": "Testpassword",
        }

        for i in range(django.conf.settings.MAX_FAILED_LOGIN_ATTEMPTS):
            self.client.post(
                django.shortcuts.reverse("users:login"),
                data=form_data_incorrect,
                follow=True,
            )

        self.assertEqual(len(django.core.mail.outbox), mail_counts + 1)

    @freezegun.freeze_time("2023-03-19 00:00:01")
    def test_over_login_activate_in_time(self):
        self.registrate_user()

        form_data_incorrect = {
            "username": "testusername",
            "password": "Testpassword",
        }

        for i in range(django.conf.settings.MAX_FAILED_LOGIN_ATTEMPTS):
            self.client.post(
                django.shortcuts.reverse("users:login"),
                data=form_data_incorrect,
                follow=True,
            )

        email_body = django.core.mail.outbox[0].body

        with freezegun.freeze_time("2023-03-25 23:30:00"):
            self.client.get(
                django.urls.reverse(
                    "users:back_activate",
                    kwargs={"activation_code": email_body.split("/")[-1]},
                )
            )

            self.assertEqual(
                django.contrib.auth.models.User.objects.get(
                    username="testusername"
                ).is_active,
                True,
            )

    @freezegun.freeze_time("2023-03-19 00:00:01")
    def test_over_login_activate_out_of_time(self):
        self.registrate_user()
        form_data_incorrect = {
            "username": "testusername",
            "password": "Testpassword",
        }

        for i in range(django.conf.settings.MAX_FAILED_LOGIN_ATTEMPTS):
            self.client.post(
                django.shortcuts.reverse("users:login"),
                data=form_data_incorrect,
                follow=True,
            )

        email_body = django.core.mail.outbox[0].body

        with freezegun.freeze_time("2023-03-26 00:30:00"):
            self.client.get(
                django.urls.reverse(
                    "users:back_activate",
                    kwargs={"activation_code": email_body.split("/")[-1]},
                )
            )

            self.assertEqual(
                django.contrib.auth.models.User.objects.get(
                    username="testusername"
                ).is_active,
                False,
            )
