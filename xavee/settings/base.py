"""
Created on May 15, 2014

@author: Kristian

Django base settings for this project. These are active when running remotely.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import dj_database_url
from datetime import date, timedelta

# Helper function to get the absolute file path to the project.
here = lambda * x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
PROJECT_ROOT = here("..")

# Function to append the root to a directory.
root = lambda * x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)

# Disable debugging on the production server! But if needed we can enable/disable debugging on Heroku:
# heroku config:add DJANGO_DEBUG=true
# heroku config:remove DJANGO_DEBUG
DEBUG          = bool(os.environ.get('DJANGO_DEBUG', ''))
TEMPLATE_DEBUG = DEBUG

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

# ====================================
#    Django REST Framework settings
# ====================================
REST_FRAMEWORK = {
    'PAGINATE_BY': 25,
    'DEFAULT_FILTER_BACKENDS':  ('rest_framework.filters.DjangoFilterBackend',),
    
    # This disables the browsable API.
    # 'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', )              
}


# ====================================
#         Celery settings
# ====================================
CELERY_ACCEPT_CONTENT    = ['json']
CELERY_TASK_SERIALIZER   = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE          = 'Japan'


# ====================================
#       Amazon AWS settings
# ====================================
AWS_ACCESS_KEY_ID       = os.environ.get('AWS_ACCESS_KEY_ID', '') #passwords.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY   = os.environ.get('AWS_SECRET_ACCESS_KEY', '') #passwords.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = 'xavee'
AWS_IS_GZIPPED          = True
AWS_PRELOAD_METADATA    = True
AWS_QUERYSTRING_AUTH    = False

ten_years = date.today() + timedelta(days=365*10)

AWS_HEADERS = {
    # Static content expires 10 years in the future at 8PM GMT.
    'Expires': ten_years.strftime('%a, %d %b %Y 20:00:00 GMT'),
    # Retrieve content from browser cache for 24 hours after the first access.
    'Cache-Control': 'max-age=86400',
}

# Storage controllers for Amazon S3.
DEFAULT_FILE_STORAGE    = 'xavee.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE     = 'xavee.s3utils.CachedStaticRootS3BotoStorage'

# GZIP_CONTENT_TYPES = (
#     'text/css',
#     'application/javascript',
#     'application/x-javascript',
#     'text/javascript'
# )

# Paths on Amazon S3.
MEDIA_URL          = 'https://xavee.s3.amazonaws.com/media/'
STATIC_URL         = 'https://xavee.s3.amazonaws.com/static/'
ADMIN_MEDIA_PREFIX = 'https://xavee.s3.amazonaws.com/static/admin/'


# ====================================
#     Django Compressor settings
# ====================================
# COMPRESS_STORAGE     = 'compressor.storage.GzipCompressorFileStorage'
COMPRESS_STORAGE     = STATICFILES_STORAGE
COMPRESS_URL         = STATIC_URL
COMPRESS_ROOT        = root("..", "assets")
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter', ]
COMPRESS_ENABLED     = True


# ====================================
#         CKEditor settings
# ====================================
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [      'Source', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', 'Templates', 'document',
              '-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', 'Undo', 'Redo',
              '-', 'Find', 'Replace', 'SelectAll', 'Scayt',
              '-', 'CreatePlaceholder', 'Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe', 'InsertPre',
              '-', 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField',
            ],
            [      'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', 'RemoveFormat',
              '-', 'NumberedList', 'BulletedList', 'Outdent', 'Indent', 'Blockquote', 'CreateDiv', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', 'BidiLtr', 'BidiRtl',
              '-', 'Link', 'Unlink', 'Anchor',
            ],
            [      'Styles', 'Format', 'Font', 'FontSize',
              '-', 'TextColor', 'BGColor',
              '-', 'UIColor', 'Maximize', 'ShowBlocks',
            ]
        ],
        'height': 440,
        'width': 755,
    },
}


# ====================================
#        Google Analytics code
# ====================================
GA_CODE = 'UA-51423008-2'


# ====================================
#     Domain/URL routing settings
# ====================================

# The default URLConf that will route all incoming requests.
ROOT_URLCONF = "xavee.urls"

HOST_MIDDLEWARE_URLCONF_MAP = {
    # App-install part of the site. We want a different router for it so that it can only access its own part.
    "www.app-install.info": "referrer.urls",
}

# Host to prepend to our generated referral links.
REFERRAL_HOST = "http://www.app-install.info"

# Hosts allowed to connect to our site.
ALLOWED_HOSTS = [ '.herokuapp.com', '.app-install.info', '.xavee.net', ]

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# ====================================
#       Localization settings
# ====================================
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# Although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Japan'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('ja', gettext('Japanese')),
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Path for the translation files.
LOCALE_PATHS = (
    root("..", "locale"),
)

# Additional locations of static files. We put everything in the assets/ dir.
STATICFILES_DIRS = (
    root("..", "assets"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#   'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'xavee.context_processors.google_analytics',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
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


# ====================================
#          Installed Apps
# ====================================
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
    'grappelli',
    'ckeditor',
    'django.contrib.admin',
    'rest_framework',
    'modeltranslation',
)

LOCAL_APPS = (
    'application',
    'blog',
    'core',
    'referrer',
    'storages',
    'compressor',
    'collectfast',
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

# ====================================
#         Grappelli settings
# ====================================
GRAPPELLI_ADMIN_TITLE = "Xavee Admin Panel"

