import dj_database_url
import os
import sys

DEBUG = False
TEMPLATE_DEBUG = DEBUG

REPO_ROOT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), '..'
))

try:
    ADMINS = (
        (os.environ['ADMIN_CONTACT_NAME'], os.environ['ADMIN_CONTACT_EMAIL']),
    )
except KeyError:
    sys.stderr.write("Ran into a problem with your admin contact settings.\n")
    ADMINS = ()

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
CACHES = {'default': {'BACKEND': 'django_pylibmc.memcached.PyLibMCCache'}}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
MEDIA_ROOT = ''
MEDIA_URL = ''

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
try:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    STATIC_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
except KeyError:
    sys.stderr.write("Ran into a problem with your S3 settings.\n")
    sys.exit(1)

STATIC_ROOT = ''
STATICFILES_DIRS = (
    os.path.join(REPO_ROOT, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
try:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
except KeyError:
    sys.stderr.write("Ran into a problem with your secret key.\n")
    sys.exit(1)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'membermash.urls'
WSGI_APPLICATION = 'membermash.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(REPO_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'gunicorn',
    'storages',
    'membermash.legislators',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
