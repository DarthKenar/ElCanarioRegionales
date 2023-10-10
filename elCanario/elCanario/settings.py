import os
from django.urls import reverse_lazy
"""
Django settings for elCanario project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ca1=v!^hnf)sqqwze==dn&8@y-1z%=j0f1kwhagbvm+$bq8^tw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pwa',
    'widget_tweaks'
]
# Apps de terceros
INSTALLED_APPS += [
    "components",
    "slippers",
]
#own apps
INSTALLED_APPS += [
    'articles',
    'customers',
    'dollar',
    'orders',
    'expenses',
    'messageslog'
]

INSTALLED_APPS += [    # The following apps are required:

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    ]

#For development
# DEV_INSTALLED_APPS = [
#     'django_extensions'
#     ]

# INSTALLED_APPS += DEV_INSTALLED_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'elCanario.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'articles/templates/articles/',
                 BASE_DIR / 'articles/templates/articles/partials',
                 BASE_DIR / 'articles/templates/articles/htmx',
                 BASE_DIR / 'orders/templates/orders', 
                 BASE_DIR / 'orders/templates/orders/partials', 
                 BASE_DIR / 'orders/templates/orders/htmx', 
                 BASE_DIR / 'customers/templates/customers', 
                 BASE_DIR / 'customers/templates/customers/partials', 
                 BASE_DIR / 'customers/templates/customers/htmx', 
                 BASE_DIR / "settings/templates/settings",
                 BASE_DIR / "settings/templates/settings/htmx",
                 BASE_DIR / "messageslog/templates/messageslog/",
                 BASE_DIR / "elCanario/templates/elCanario/",
                 BASE_DIR / "components/templates/molecules",
                 BASE_DIR / "_core/templates/_core",
                 BASE_DIR / "allauth/templates/"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            "builtins": ["slippers.templatetags.slippers"],  # Slippers
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'elCanario.wsgi.app'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'verceldb',
#         'USER': 'default',
#         'PASSWORD': 'ktL5rIxR4XVJ',
#         'HOST': 'ep-floral-sound-641112-pooler.us-east-1.postgres.vercel-storage.com',
#         'PORT': '5432',
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'USER': 'postgres',
#         'PASSWORD': '9875410',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#         'OPTIONS':{
#             'options': '-c search_path=public',
#             'dbname': os.path.join(BASE_DIR, 'regionales'),
#         }
#     }
# }

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

SITE_ID = 1

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Buenos_Aires'

USE_I18N = True

USE_TZ = True

# Allauth

LOGIN_REDIRECT_URL = reverse_lazy('core:home')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"  # Nuevo

STATIC_ROOT = BASE_DIR / "static/"  # Nuevo

STATICFILES_DIRS = [
    BASE_DIR / "staticfiles",
    BASE_DIR.parent / "node_modules",
]  # Nuevo

TE_URL = "node_modules/"  # Nuevo


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

PWA_APP_NAME = "EL CANARIO REGIONALES"
PWA_APP_DESCRIPTION = "For Luci whit <3"
PWA_APP_THEME_COLOR = '#991b1b'
PWA_APP_BACKGROUND_COLOR = '#fde68a'

PWA_APP_ICONS = [
    {
        "src": "static/img/elcanarioregionales-logo-160x160.png",
        "sizes": "160x160"
    }
]

PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR,'serviceworker.js')
