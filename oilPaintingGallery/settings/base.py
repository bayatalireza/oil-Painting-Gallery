from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    #Local apps

    'apps.accounts.apps.AccountsConfig',
    'apps.artworks.apps.ArtworksConfig',
    'apps.orders.apps.OrdersConfig',
    'apps.reviews.apps.ReviewsConfig',
    'apps.dashboard.apps.DashboardConfig',
    # امنیت
    'axes',        # قفل‌کردن حساب پس از تلاش‌های ناموفق ورود
    'csp',          # هدر Content-Security-Policy
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'axes.middleware.AxesMiddleware',   # باید آخرین middleware باشد
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',   # باید اول باشد
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'accounts.User'

ROOT_URLCONF = 'oilPaintingGallery.urls'

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

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- محدودیت آپلود فایل (بخش ۳.۵) ---
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024       # ۵ مگابایت
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

# --- django-axes (محافظت در برابر Brute-Force لاگین) ---
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1   # ۱ ساعت قفل پس از ۵ تلاش ناموفق
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']