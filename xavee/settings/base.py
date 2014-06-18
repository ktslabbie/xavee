"""
Created on May 15, 2014

@author: Kristian

Django settings for this project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import dj_database_url

# Helper function to get the absolute file path to the project.
here = lambda * x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
PROJECT_ROOT = here("..")

# Function to append the root to a directory.
root = lambda * x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)

# Disable debugging on the production server!
DEBUG          = False
TEMPLATE_DEBUG = False

# Admins for the admin console.
ADMINS = (
    ("Kristian Slabbekoorn", "kristian@agent-solve.com"),
)

# Managers are also admins.
MANAGERS = ADMINS

# Configure the database for Heroku.
DATABASES = {
    'default': dj_database_url.config()
}

REST_FRAMEWORK = {
    'PAGINATE_BY': 10              
}

# ID for the sites framework.
#SITE_ID = 1

# Google Analytics code. Will be inserted automatically into the HTML5 Boilerplate code.
DH5BP_GA_CODE = 'UA-51423008-2'

# The default URLConf that will route all incoming requests.
ROOT_URLCONF = "xavee.urls"

HOST_MIDDLEWARE_URLCONF_MAP = {
    # App-install part of the site. We want a different router for it so that it can only access its own part.
    "www.app-install.info": "referrer.urls",
}

# Host to prepend to our generated referral links.
REFERRAL_HOST = "http://www.app-install.info"

# Hosts allowed to connect to our site.
ALLOWED_HOSTS = [ '.herokuapp.com', '.app-install.info', ]

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# Although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Japan'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = root("..", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = root("..", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    root("..", "assets"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    'django.contrib.messages.context_processors.messages',
    'xavee.context_processors.google_analytics',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8w)3$4m03*0almq)0yercyj%07@%d)fvc32rf4,,.few3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'xavee.multihost.MultiHostMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'xavee.wsgi.application'

TEMPLATE_DIRS = (
    root("templates"),
)

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
#    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'south',
    'dh5bp',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'rest_framework',
)

LOCAL_APPS = (
    'application',
    'blog',
    'referrer',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

# Grappelli settings:
GRAPPELLI_ADMIN_TITLE = "Xavee Admin Panel"
