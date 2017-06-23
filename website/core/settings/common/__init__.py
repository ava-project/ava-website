import os
from . import apps_in_folder

env = os.environ

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
BASE_DIR = '/app'
DEBUG = True
SECRET_KEY = env.get('SECRET_KEY', 'weird punchy keyboard')
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'
SITE_ID = 1

from .apps import *
from .auth import *
from .database import *
from .files import *
from .middleware import *
from .template import *
from .zone import *
