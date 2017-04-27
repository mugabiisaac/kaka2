"""
Django settings for kaka2 project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.core.mail import send_mail
#import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3*nk71k4eg@+p)+^@zz9%xt@rt6ir9l8p+@#8b5t-*xz@lkzjb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['www.kaka2.co', 'kaka2.co']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',
    'home',
    'easy_thumbnails',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kaka2.urls'
ROOT_HOSTCONF ='kaka.hosts'
DEFAULT_HOST ='www'
DEFAULT_REDIRECT_URL = "http://www.kaka2.co"
PARENT_HOST = "kaka2.co"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'template')],
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

WSGI_APPLICATION = 'kaka2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ACCOUNT_ACTIVATION_DAYS = 7

AUTH_PROFILE_MODULE = 'user_profile.UserProfile'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = [

    #os.path.join(BASE_DIR, STATIC_URL),


    os.path.join(BASE_DIR, "static"),
    #'/static/'

]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'trayforduganda@gmail.com'
EMAIL_HOST_PASSWORD = 'Kisitu1234'
SERVER_EMAIL = 'trayforduganda@gmail.com'
DEFAULT_FORM_EMAIL = 'blog'

MEDIA_ROOT = os.path.join(BASE_DIR, "media_cdn")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")


LOGIN_REDIRECT_URL = '/posts/'

LOGOUT_REDIRECT_URL = '/'


INITIAL_ORDER_STATUS = 'Pending'
INITIAL_LINE_STATUS = 'Pending'
ORDER_STATUS_PIPELINE ={
    'Pending': ('Being processed', 'Cancelled',),
    'Being Processed': ('Processed', 'cancelled',),
    'Cancelled': (),
}

# Update database configuration with $DATABASE_URL.
#db_from_env = dj_database_url.config(conn_max_age=500)
#DATABASES['default'].update(db_from_env)

#STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#export DJANGO_SETTINGS_MODULE=kaka2.settings
#heroku config:set DJANGO_SETTINGS_MODULE=kaka2.settings --account personal
