import os
from distutils.util import strtobool
from pathlib import Path

from celery.schedules import crontab

from config.utils import get_env_value

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.environ.get('LOG_DIR', os.path.join(BASE_DIR, 'logs'))
SECRET_KEY = get_env_value('SECRET_KEY')
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.environ.get('DJANGO_DEBUG', 'False'))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(' ')
HOSTNAME = get_env_value('SITE_HOSTNAME')

COINMARKET_KEY = get_env_value('COINMARKET_KEY')
COINMARKET_CURRENCY = get_env_value('COINMARKET_CURRENCY')
TARGET_CURRENCY = os.environ.get('TARGET_CURRENCY', '')

# eMail-Settings
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
if os.environ.get('EMAIL_HOST_USER', ''): EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
if os.environ.get('EMAIL_HOST_PASSWORD', ''): EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = strtobool(os.environ.get('EMAIL_USE_TLS', 'False'))
EMAIL_USE_SSL = strtobool(os.environ.get('EMAIL_USE_SSL', 'True'))
EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_DISPLAY = os.environ.get('EMAIL_DISPLAY', os.environ.get('EMAIL_SENDER'))
EMAIL_SUBJECT_PREFIX = os.environ.get('EMAIL_SUBJECT_PREFIX')
SERVER_EMAIL = os.environ.get('EMAIL_SENDER')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_SENDER')
EMAIL_TIMEOUT = 15

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_celery_beat',  # Celery Schedule
    'django_celery_results',  # Track & Trace
    'django_htmx',  # Request HTMX Enrichment
]

LOCAL_APPS = [
    'crypto'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_value('POSTGRES_DB'),
        'USER': get_env_value('POSTGRES_USER'),
        'PASSWORD': get_env_value('POSTGRES_PASSWORD'),
        'HOST': get_env_value('POSTGRES_HOST'),
        'PORT': get_env_value('POSTGRES_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Static Content
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'crypto', 'static'),
]

# User defined media content (Profile pictures)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_files')
MEDIA_URL = '/media/'

# Login Settings
LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = 'core:landing'
# LOGOUT_REDIRECT_URL = 'core:landing'

# Session Settings
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = strtobool(os.environ.get('SESSION_COOKIE_HTTPONLY', 'True')) # no JavaScript can access
SESSION_COOKIE_SECURE = strtobool(os.environ.get('SESSION_SECURE', 'True'))  # only HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = strtobool(os.environ.get('SESSION_EXPIRE_AT_BROWSER_CLOSE', 'True'))
SESSION_COOKIE_AGE = eval(os.environ.get('SESSION_COOKIE_AGE', 60*60*1))  # 1h Timeout


USE_I18N = False
USE_L10N = False
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'de-DE'
TIME_ZONE = os.environ.get('TZ', 'Europe/Berlin')
DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y H:i:s'
DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%d.%m.%Y %H:%M:%S',     # '25.10.2006 14:30:59'
    '%d.%m.%Y %H:%M:%S.%f',  # '25.10.2006 14:30:59.000200'
    '%d.%m.%Y %H:%M',        # '25.10.2006 14:30'
    '%d.%m.%Y',              # '25.10.2006'
]

DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%d.%m.%Y',    # '2006-10-25', '25.10.2006',
    '%d %b %Y', '%d %b, %Y',   # '25 Oct 2006', '25 Oct, 2006'
    '%d. %B %Y', '%d. %B, %Y', # '25. October 2006', '25. October, 2006'
]

SHORT_DATE_FORMAT = 'd.m.Y'
TECHNICAL_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'd.m.Y, H:i'
DECIMAL_SEPARATOR = ','
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'

# Celery
# ------------------------------------------------------------------------------
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
if USE_TZ: CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = get_env_value('CELERY_BROKER_URL')
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = 'django-db'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ['json']
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']  # noqa F405
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa F405
    INTERNAL_IPS = ['127.0.0.1']


CELERY_BEAT_SCHEDULE = {
    'crypto_update': {
        'task': 'crypto.tasks.crypto_update_task',
        'schedule': crontab(minute='*/5'),
    },
}
