from . import *  # noqa

import dj_database_url

import os


DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASES['default'] = dj_database_url.config(  # noqa
    conn_max_age=600,
    ssl_require=True,
)

# Include Django-Heroku at the end of the file
import django_heroku  # noqa
django_heroku.settings(locals())
