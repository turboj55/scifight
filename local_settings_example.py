# This file is a template for 'local_settings.py' which can be useful when
# configuring developer's environment. If your setup is as simple as local
# MariaDB instance, just do:
#
#    $ cp local_settings_example.py local_settings.py
#    $ vim local_settings.py
#
# And manually adjust your secret key and database credentials. Consider
# removing this comment, though.
from scifight_proj.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
# You can generate secret key on this site:
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = 'your_secret_key'

# Example database options for MySQL (or MariaDB).
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'scifight',
        'USER':     'user',
        'PASSWORD': 'password',
        'HOST':     'localhost',
        'PORT':     3306
    }
}

LANGUAGE_CODE = 'en-US'

DEBUG = True

ALLOWED_HOSTS = []
