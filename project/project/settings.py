import os
import pathlib

import dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

dotenv.load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-w30sdst!pi!e$n00rf4iu@')


DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1')


ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    '127.0.0.1',
).split(',')

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'home.apps.HomeConfig',
    'dishes.apps.DishesConfig',
    'feedback.apps.FeedbackConfig',
    'core.apps.CoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'tz_detect',
    'taggit',
    'taggit_selectize',
    'tinymce',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'project.middleware.custom.RateLimitMiddleware',
]

RATE_LIMIT_MIDDLEWARE = os.getenv(
    'RATE_LIMIT_MIDDLEWARE', 'False'
).lower() in (
    'active',
    'true',
    '1',
)

REQUESTS_PER_SECOND = int(os.getenv('REQUESTS_PER_SECOND', 10))

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.' 'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

LANGUAGES = [
    ('ru', 'Russian'),
    ('en', 'English'),
]

TZ_DETECT_COUNTRIES = ('RU', 'US', 'JP')

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if DEBUG:
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)


INTERNAL_IPS = [
    '127.0.0.1',
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'users.backends.AuthByEmailOrUsernameBackend',
]

ACTIVATE_USERS = (
    True if DEBUG else os.getenv('ACTIVATE_USERS', 'False').lower() == 'true'
)

MAX_FAILED_LOGIN_ATTEMPTS = int(os.getenv('MAX_FAILED_LOGIN_ATTEMPTS', 3))


LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = LOGIN_URL

TAGGIT_CASE_INSENSITIVE = True
TAGGIT_TAGS_FROM_STRING = 'taggit_selectize.utils.parse_tags'
TAGGIT_STRING_FROM_TAGS = 'taggit_selectize.utils.join_tags'

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'modern',
    'width': 'auto',
    'plugins': [
        'advlist autolink lists charmap print preview hr anchor',
        'searchreplace wordcount nonbreaking save fullscreen',
        'emoticons template paste textcolor colorpicker textpattern',
    ],
    'toolbar1': (
        'undo redo | '
        'bold italic underline strikethrough | '
        'alignleft aligncenter alignright alignjustify | '
        'bullist numlist outdent indent | '
        'forecolor backcolor'
    ),
    'toolbar2': (
        'styleselect formatselect fontselect fontsizeselect | '
        'emoticons | '
        'preview'
    ),
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'send_mail'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'true').lower() == 'true'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'true').lower() == 'true'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mail.ru')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 2525))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your@mail.ru')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'password')
