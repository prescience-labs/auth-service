import logging
import os

import dj_database_url
from django.utils.log import DEFAULT_LOGGING

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

SEVEN_DAYS  = 604800 # seconds
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY                  = os.getenv('SECRET_KEY')
DEBUG                       = os.getenv('DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS               = os.getenv('ALLOWED_HOSTS', 'localhost,0.0.0.0').split(',')
CORS_ORIGIN_ALLOW_ALL       = os.getenv('CORS_ORIGIN_ALLOW_ALL', 'false').lower() == 'true'
CORS_ORIGIN_WHITELIST       = os.getenv('CORS_ORIGIN_WHITELIST').split(',') if os.getenv('CORS_ORIGIN_WHITELIST') else []
CORS_ORIGIN_REGEX_WHITELIST = os.getenv('CORS_ORIGIN_REGEX_WHITELIST') if os.getenv('CORS_ORIGIN_REGEX_WHITELIST') else []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'oauth2_provider',
    'corsheaders',

    'common.apps.CommonConfig',
    'v1.apps.V1Config',
]

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    # Uncomment following if you want to access the admin
    'django.contrib.auth.backends.ModelBackend'
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'common.services.token.jwt_middleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'
APPEND_SLASH=False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME':     os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)


# Authentication
AUTH_USER_MODEL                     = 'common.User'
PASSWORD_RESET_EXPIRATION_MINUTES   = 60
TOKEN_EXPIRATION_PERIOD             = 7 # days
# LOGIN_URL                           = 'auth_login'

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read':             'Read scope',
        'write':            'Write scope',
        'introspection':    'Introspect token scope',
    },

    'CLIENT_ID_GENERATOR_CLASS':            'oauth2_provider.generators.ClientIdGenerator',
    'ALLOWED_REDIRECT_URI_SCHEMES':         ['http', 'https'],
    'AUTHORIZATION_CODE_EXPIRE_SECONDS':    600,
    'REFRESH_TOKEN_EXPIRE_SECONDS':         SEVEN_DAYS,
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
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


# Internationalization
LANGUAGE_CODE   = 'en-us'
TIME_ZONE       = 'UTC'
USE_I18N        = True
USE_L10N        = True
USE_TZ          = True


# Static files (CSS, JavaScript, Images)
STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Django Rest Framework
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':                50,
    'EXCEPTION_HANDLER':        'common.services.exceptions.api_error_handler',
}
SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'list',
}

# Email
DEFAULT_FROM_EMAIL  = os.getenv('FROM_EMAIL', 'no-reply@example.com')
EMAIL_HOST          = os.getenv('EMAIL_HOST', 'smtp.ethereal.email')
EMAIL_PORT          = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER', 'tpll5wiiajplpxd6@ethereal.email')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'KPh5WESzRuQETtRgHq')
EMAIL_HOST_USE_SSL  = os.getenv('EMAIL_HOST_USE_SSL', 'false').lower() == 'true'

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()
LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(levelname)-8s %(asctime)s %(name)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class':        'logging.StreamHandler',
            'formatter':    'console',
        },
    },
    'loggers': {
        # root logger
        '': {
            'level':        LOG_LEVEL,
            'handlers':     ['console'],
        },
        'django.utils.autoreload': {
            'level': 'INFO',
        },
        'django.db.backends': {
            'level': 'INFO',
        },
    },
})
