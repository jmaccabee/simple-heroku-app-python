import os

from . import *  # noqa


DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
