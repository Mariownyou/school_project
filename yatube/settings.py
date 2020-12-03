import os
from .utils import generate_uuid4_filename


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '1@m(&f1ri9e)l#=(*+uz=s_%sfxoniln8rwo3_cl+7)uz40t#%'

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
    "testserver",
    '67dbadabfc9d.ngrok.io'
]

INSTALLED_APPS = [
    'users',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'trumbowyg',
    'ckeditor_uploader',
    'posts',
    'forms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yatube.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

WSGI_APPLICATION = 'yatube.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

TRUMBOWYG_THUMBNAIL_SIZE = (100, 100)
TRUMBOWYG_TRANSLITERATE_FILENAME = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '/auth/login/'

LOGIN_REDIRECT_URL = 'index'

LOGOUT_REDIRECT_URL = 'index'

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

EMAIL_HOST = 'smtp.gmail.com'
DEFAULT_FROM_EMAIL = 'smj510black@gmail.com'
SERVER_EMAIL = 'smj510black@gmail.com'
EMAIL_HOST_USER = 'smj510black@gmail.com'
EMAIL_HOST_PASSWORD = 'qmkoczzpzccvqdzt'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SITE_ID = 1

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
