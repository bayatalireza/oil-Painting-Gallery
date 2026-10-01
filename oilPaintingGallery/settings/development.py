from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# در توسعه، ایمیل‌ها به کنسول چاپ می‌شوند نه ارسال واقعی
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'