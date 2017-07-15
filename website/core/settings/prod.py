import ast

from .common import *

DEBUG = False

ALLOWED_HOSTS = ['www.ava-project.com', 'ava-project.com', '163.5.84.224']

# email configuration
EMAIL_HOST = env.get('EMAIL_HOST', '')
EMAIL_PORT = int(env.get('EMAIL_PORT', 0))
EMAIL_HOST_USER = env.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = ast.literal_eval(env.get('EMAIL_USE_TLS', True))
DEFAULT_FROM_EMAIL = 'contact@ava-project.com'

# config sentry logging
SENTRY_KEY = env.get('SENTRY_KEY', None)
if SENTRY_KEY:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')
    RAVEN_CONFIG = {'dsn': SENTRY_KEY}
