################################################################################
#
# File Name: settings.py
# Application: mgi
# Description: 
#   Django settings for mgi project.
#   For more information on this file, see
#   https://docs.djangoproject.com/en/1.6/topics/settings/
#
#   For the full list of settings and their values, see
#   https://docs.djangoproject.com/en/1.6/ref/settings/
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

VERSION = "1.1.1"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#SPARQL project URI
PROJECT_URI = "http://www.example.com/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = ['*']

# HTTPS: Enable these options when HTTPS set up
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.request",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages")

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mongoengine.django.mongo_auth',
    'admin_mdcs',
    'curate',
    'explore',
    'compose',
    'rest_framework',  # djangorestframework
    'rest_framework_swagger', #django-rest-swagger for api documentation
    'api', # djangorestframework
    'oauth2_provider',
)

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'}
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": ['error_redirect','ping'], # List URL namespaces to ignore
    "api_version": '1.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}


# django.contrib.auth.views.login redirects you to accounts/profile/ 
# right after you log in by default. This setting changes that.
LOGIN_REDIRECT_URL = '/'


#http://docs.mongoengine.org/en/latest/django.html
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
#SESSION_ENGINE = "django.contrib.sessions.backends.file"
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_SAVE_EVERY_REQUEST=True
SESSION_EXPIRE_AT_BROWSER_CLOSE=True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',  # https://docs.djangoproject.com/en/dev/howto/auth-remote-user/
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mgi.urls'

WSGI_APPLICATION = 'mgi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
#     'default': {
# #         'ENGINE': 'django.db.backends.dummy'
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER':"postgres",
        'PASSWORD': "data123",
        'NAME': 'mgi',                      
    }
}

# AUTHENTICATION_BACKENDS = (
#     'mongoengine.django.auth.MongoEngineBackend',
# )

# AUTH_USER_MODEL = 'mongo_auth.MongoUser'
# MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'

from mongoengine import connect
MONGODB_URI = "mongodb://admin:admin@localhost/mgi"
connect("mgi", host=MONGODB_URI)


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# python manage.py collectstatic gathers all static files in this directory
# link this directory to static in apache configuration file
STATIC_ROOT = 'var/www/mgi/static/'

# static files manually added
STATIC_URL = '/static/'

# static files gathered
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Django User Roles Package
# https://github.com/dabapps/django-user-roles

USER_ROLES = (
    'scientist',
    'sysadmin',
)

# Logging
# https://docs.djangoproject.com/en/1.6/topics/logging/

SITE_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..').replace('\\', '/')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': SITE_ROOT + "/logfile",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {  # use 'MYAPP' to make it app specific
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}