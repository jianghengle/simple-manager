import os
from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('RDS_DB_NAME', 'simple_manager'),
        'USER': os.environ.get('RDS_USERNAME', 'postgres'),
        'PASSWORD': os.environ.get('RDS_PASSWORD', 'postgres'),
        'HOST': os.environ.get('RDS_HOSTNAME', 'localhost'),
        'PORT': os.environ.get('RDS_PORT', 5432),
    }
}

# AWS
ACCESS_KEY_ID = os.environ.get('ACCESS_KEY_ID', 'access')
SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY', 'secret')

WEB_APP_DOMAIN = os.environ.get('WEB_APP_DOMAIN', 'http://localhost:8000')
INVOICE_APPROVAL_RECIPENTS = os.environ.get('INVOICE_APPROVAL_RECIPENTS', '')
