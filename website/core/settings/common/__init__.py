import os
from . import apps_in_folder

env = os.environ

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
BASE_DIR = '/app'
DEBUG = True
SECRET_KEY = env.get('SECRET_KEY', 'weird punchy keyboard')
STATIC_URL = '/static/'
STATIC_ROOT = '/app/public'
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'
MEDIA_ROOT = '/data'

SITE_ID = 1

from .apps import *
from .auth import *
from .database import *
from .middleware import *
from .template import *
from .uploads import *
from .zone import *
