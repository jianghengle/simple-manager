from .base import *
import environ

env = environ.Env()
environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
    }
}

# AWS
ACCESS_KEY_ID = env('ACCESS_KEY_ID')
SECRET_ACCESS_KEY = env('SECRET_ACCESS_KEY')

WEB_APP_DOMAIN = env('WEB_APP_DOMAIN')
INVOICE_APPROVAL_RECIPENTS = env('INVOICE_APPROVAL_RECIPENTS')
