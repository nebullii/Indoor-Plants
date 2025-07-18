"""
Django settings for indoor_plant project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import dj_database_url
from pathlib import Path
import environ
import os
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")

STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['nevus.pythonanywhere.com', 'localhost', '127.0.0.1', '*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # Required for flatpages
    "django.contrib.flatpages",  # Required for flatpages
    "accounts",  # Simplified app inclusion
    "indoor_plant",
    'widget_tweaks',
    'products',
    'cart',
    'orders',
    'payments',
    'django_countries',
    'admin_dashboard',
    'explorer',
    'ai',    
    'analytics',
    'ckeditor',
    'django_quill',
    'inventory',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    'django.contrib.sessions.middleware.SessionMiddleware',
    'analytics.middleware.LogSiteVisitMiddleware',
    'analytics.middleware.LogPageViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',  # Add this line
]

ROOT_URLCONF = "indoor_plant.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'products.context_processors.categories',
            ],
        },
    },
]

WSGI_APPLICATION = "indoor_plant.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# Database settings
if os.environ.get('PYTHONANYWHERE_DOMAIN'):
    # PythonAnywhere database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'nevus$default',
            'USER': 'nevus',
            'PASSWORD': 'pythonAnywhere',
            'HOST': 'nevus.mysql.pythonanywhere-services.com',
            'PORT': '3306',
        }
    }
else:
    # Local database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'indoor_plant',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


AUTH_USER_MODEL = 'accounts.CustomUser'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "home"  # redirect to home after login
LOGOUT_REDIRECT_URL = "home"  # redirect to home after logout 

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files (User-uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGOUT_REDIRECT_URL = 'home'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Security settings
SECURE_SSL_REDIRECT = False  # Disable SSL redirect for free tier
SESSION_COOKIE_SECURE = False  # Disable secure cookies for free tier
CSRF_COOKIE_SECURE = False  # Disable secure CSRF cookies for free tier
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

if not STRIPE_PUBLISHABLE_KEY or not STRIPE_SECRET_KEY:
    raise ImproperlyConfigured('Stripe API keys are not set in environment variables')

SHIPPING_COST = 5.00

# Add SITE_ID setting
SITE_ID = 1

EXPLORER_PERMISSION_VIEW = lambda request: (
    request.user.is_authenticated and (
        getattr(request.user, 'role', None) == 'SELLER' or
        request.user.is_staff or
        request.user.is_superuser
    )
)

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'extraPlugins': ','.join([
            'codesnippet',  # if you want code blocks
        ]),
        'removePlugins': 'stylesheetparser',
        'allowedContent': True,
    }
}
