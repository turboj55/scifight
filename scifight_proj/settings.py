"""
Django settings for scifight project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import logging
from .settings_secret import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_PATH = os.path.join(BASE_DIR, 'scifight.log')
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# '
                           u'%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG,
                    filename=LOG_PATH)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'scifight',
    'admin_reorder',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder'
]

ROOT_URLCONF = 'scifight_proj.urls'

WSGI_APPLICATION = 'scifight_proj.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

ADMIN_REORDER = ('sites',
    dict(app='scifight',
         label='Tournament preparation',
         models=[
             'scifight.Team',
             'scifight.Participant',
             'scifight.Leader',
             'scifight.Room',
             'scifight.Problem',
             'scifight.Jury',
             'scifight.LeaderToJury',
             'scifight.TeamOrigin',
             'scifight.CommonOrigin']),

    dict(app='scifight',
         label='Tournament progress',
         models=[
             'scifight.Fight',
             'scifight.FightStage']),

    dict(app='scifight',
         label='Website administration',
         models=[
            'scifight.Tournament',
            'auth.User',
            'auth.Group']))
