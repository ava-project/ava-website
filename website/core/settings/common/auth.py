LOGIN_REDIRECT_URL = '/user/profile'
LOGIN_URL = '/user/login'
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'user.backend.AuthenticationBackend',
    'user.backend.EmailBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
