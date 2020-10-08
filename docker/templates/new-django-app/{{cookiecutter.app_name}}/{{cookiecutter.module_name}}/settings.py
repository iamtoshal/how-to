"""
Django settings for example_app project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from {{cookiecutter.module_name}}.logging import before_send

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Retrieve the secret key from the DJANGO_SECRET_KEY environment variable
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Set the DJANGO_DEBUG environment variable to False to disable debug mode
DEBUG = False if os.getenv('DJANGO_DEBUG', True) == 'False' else True

# Define DJANGO_ALLOWED_HOSTS as a comma-separated list of valid hosts,
# e.g. localhost,127.0.0.1,.herokuapp.com
allowed_hosts = os.getenv('DJANGO_ALLOWED_HOSTS', [])
ALLOWED_HOSTS = allowed_hosts.split(',') if allowed_hosts else []


# Configure Sentry for error logging
if os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        before_send=before_send,
        integrations=[DjangoIntegration()],
    )

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    '{{cookiecutter.module_name}}'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{{cookiecutter.module_name}}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
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

WSGI_APPLICATION = '{{cookiecutter.module_name}}.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {}

DATABASES['default'] = dj_database_url.parse(
    os.getenv('DATABASE_URL', 'postgres://postgres:postgres@postgres:5432/{{cookiecutter.pg_db}}'),
    conn_max_age=600,
    ssl_require=True if os.getenv('POSTGRES_REQUIRE_SSL') else False{% if cookiecutter.postgis == 'True' %},
    engine='django.contrib.gis.db.backends.postgis'{% endif %}
)

# Caching
# https://docs.djangoproject.com/en/3.0/topics/cache/

cache_backend = 'dummy.DummyCache' if DEBUG is True else 'db.DatabaseCache'
CACHES = {
    'default': {
        'BACKEND': f'django.core.cache.backends.{cache_backend}',
        'LOCATION': 'site_cache',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static'
STATICFILES_STORAGE = os.getenv(
    'DJANGO_STATICFILES_STORAGE',
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Django Compressor configs
COMPRESS_PRECOMPILERS = (
    ('module', 'export NODE_PATH=/app/node_modules && npx browserify {infile} -t [ babelify --presets [ @babel/preset-env ] ] > {outfile}'),
    ('text/jsx', 'export NODE_PATH=/app/node_modules && npx browserify {infile} -t [ babelify --presets [ @babel/preset-env @babel/preset-react ] ] > {outfile}'),
)

COMPRESS_OUTPUT_DIR = 'compressor'

# Enforce SSL in production
if DEBUG is False:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
