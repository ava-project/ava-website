from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
    }
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
