import os

env = os.environ

ALLOWED_HOSTS = []
BASE_DIR = '/app'
DEBUG = True
SECRET_KEY = env.get('SECRET_KEY', 'weird punchy keyboard')
STATIC_URL = '/static/'
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

from .apps import *
from .auth import *
from .database import *
from .middleware import *
from .template import *
from .zone import *