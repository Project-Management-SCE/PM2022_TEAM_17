
   
"""
Django settings for StockFlow project.
Generated by 'django-admin startproject' using Django 4.0.3.
For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import sys
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*^@6rgitt8o-73)=rrdqg#dd5nw8y!4^$0=m-$8=nv%bf)4w9='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['stockflow-17.herokuapp.com']

#gmail email send/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'stockflowteam17@gmail.com' 
EMAIL_HOST_PASSWORD = '123team17' 
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'

# Application definition
CSRF_TRUSTED_ORIGINS = ["https://stockflow-17.herokuapp.com/"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AgentSignUp.apps.AgentsignupConfig',
    'accounts',
    'django_jenkins',
    'stocks',
]

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_jslint',
    'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_sloccount',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
)
PROJECT_APPS = ['AgentSignUp','accounts','stocks']


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'StockFlow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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


AUTH_USER_MODEL='accounts.User'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/user/accounts/'

WSGI_APPLICATION = 'StockFlow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
Testing = sys.argv[1:2] == ['test']
if not Testing:
    DATABASES = {

        'default': {
            #'tcp':'stockflow-db.database.windows.net',

            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'szleqasu',
            'USER': 'szleqasu',
            'PASSWORD': 'MnebV98dwiGY7rHhiUxxFGoMEh7VG4vO',
                # ↓ HOST instead of HOSTS
            'HOST': 'chunee.db.elephantsql.com',
            'PORT':'',
            #  'OPTIONS':{
            #      'DRIVER':'SQL Server Native Client 11.0',
            #      'dsn': 'djangodatabase',
            #      'MARS_Connection':'True',
            #  }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        "TEST": {
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }}



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'



# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configure Django App for Heroku.
