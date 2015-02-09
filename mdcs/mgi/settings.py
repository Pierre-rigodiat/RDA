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

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#SPARQL project URI
PROJECT_URI = "http://www.example.com/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ponq)(gd8hm57799)$lup4g9kyvp0l(9)k-3!em7dddn^(y)!5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = ['*']

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


#optional
MULTIUPLOADER_FILES_FOLDER = 'multiuploader'
#optional
MULTIUPLOADER_FILE_EXPIRATION_TIME = 3600
#optional
MULTIUPLOADER_FORMS_SETTINGS = {
'default': {
    'FILE_TYPES' : ["txt","zip","jpg","jpeg","flv","png"],
    'CONTENT_TYPES' : [
            'image/jpeg',
            'image/png',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/vnd.oasis.opendocument.text',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.presentation',
            'text/plain',
            'text/rtf',
                ],
    'MAX_FILE_SIZE': 10485760,
    'MAX_FILE_NUMBER':5,
    'AUTO_UPLOAD': True,
},
'images':{
    'FILE_TYPES' : ['jpg', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'tiff', 'ico' ],
    'CONTENT_TYPES' : [
        'image/gif',
        'image/jpeg',
        'image/pjpeg',
        'image/png',
        'image/svg+xml',
        'image/tiff',
        'image/vnd.microsoft.icon',
        'image/vnd.wap.wbmp',
        ],
    'MAX_FILE_SIZE': 10485760,
    'MAX_FILE_NUMBER':5,
    'AUTO_UPLOAD': True,
},
'video':{
    'FILE_TYPES' : ['flv', 'mpg', 'mpeg', 'mp4' ,'avi', 'mkv', 'ogg', 'wmv', 'mov', 'webm' ],
    'CONTENT_TYPES' : [
        'video/mpeg',
        'video/mp4',
        'video/ogg',
        'video/quicktime',
        'video/webm',
        'video/x-ms-wmv',
        'video/x-flv',
        ],
    'MAX_FILE_SIZE': 10485760,
    'MAX_FILE_NUMBER':5,
    'AUTO_UPLOAD': True,
},
'audio':{
    'FILE_TYPES' : ['mp3', 'mp4', 'ogg', 'wma', 'wax', 'wav', 'webm' ],
    'CONTENT_TYPES' : [
        'audio/basic',
        'audio/L24',
        'audio/mp4',
        'audio/mpeg',
        'audio/ogg',
        'audio/vorbis',
        'audio/x-ms-wma',
        'audio/x-ms-wax',
        'audio/vnd.rn-realaudio',
        'audio/vnd.wave',
        'audio/webm'
        ],
    'MAX_FILE_SIZE': 10485760,
    'MAX_FILE_NUMBER':5,
    'AUTO_UPLOAD': True,
}}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mongoengine.django.mongo_auth',
    'admin',
    'curate',
    'explore',
    'compose',
    'dajax',
    'dajaxice',
    'rest_framework',  # djangorestframework
    'rest_framework_swagger', #django-rest-swagger for api documentation
    'api', # djangorestframework
)
 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": ['error_redirect','ping'], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
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

#AUTH_USER_MODEL = 'mongo_auth.MongoUser'

#http://docs.mongoengine.org/en/latest/django.html
#SESSION_ENGINE = 'mongoengine.django.sessions'
#SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'
#SESSION_ENGINE = "django.contrib.sessions.backends.file"
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_SAVE_EVERY_REQUEST=True

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
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

from mongoengine import connect

connect('mgi')

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

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
    'dajaxice.finders.DajaxiceFinder',
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

if DEBUG:
    import logging
 
    logger = logging.getLogger('django_auth_ldap')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

########################################################################
# DJANGO AUTH LDAP
# http://pythonhosted.org/django-auth-ldap/index.html
########################################################################


import ldap
from django_auth_ldap.config import LDAPSearch

# AUTH_LDAP_START_TLS = True  
AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: False,
    ldap.OPT_REFERRALS: False,
} 

# Binding to the LDAP
AUTH_LDAP_SERVER_URI = "ldap://wsgendev02.gendev.nist.gov:389"  # ldap server
AUTH_LDAP_BIND_DN = "cn=ssy,ou=NISTUSERS,dc=GENDEV,dc=NIST,dc=GOV"
AUTH_LDAP_BIND_PASSWORD = "YMS*1975*smy"

#Search the user from the login inputs
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=NISTUSERS,dc=GENDEV,dc=NIST,dc=GOV", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
# AUTH_LDAP_USER_DN_TEMPLATE = "ou=NISTUSERS,dc=GENDEV,dc=NIST,dc=GOV"

# Get these attributes from the LDAP to create the Django user
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

# Try to find the user in the LDAP first, and then in the django backend
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_ALWAYS_UPDATE_USER = False
