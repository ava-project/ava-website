import ast

from .common import *

DEBUG = False

ALLOWED_HOSTS = ['www.ava-project.com', 'ava-project.com', '163.5.84.224']

EMAIL_HOST = env.get('EMAIL_HOST', '')
EMAIL_PORT = int(env.get('EMAIL_PORT', 0))
EMAIL_HOST_USER = env.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = env.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = ast.literal_eval(env.get('EMAIL_USE_TLS', True))
