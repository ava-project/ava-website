from .common import *

EMAIL_HOST = 'mail'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 1025
EMAIL_USE_TLS = False

INSTALLED_APPS.append('debug_toolbar')

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: True,
}

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
