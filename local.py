"""
Created on May 15, 2014

@author: Kristian

Local Django settings for this project. This is only called when running locally.
"""
from base import root

# Locally, we can safely run with debug turned on. Not safe for the production server!
DEBUG          = True
TEMPLATE_DEBUG = DEBUG

# ====================================
#         Celery settings
# ====================================
BROKER_URL = 'redis://localhost:6379/0'

HOST_MIDDLEWARE_URLCONF_MAP = {
    # Route to App-install part of the site. Uncomment this to test the Referrer application locally!
    # "localhost": "referrer.urls", 
}

# Disable collectfast; gives problems with S3 and offline compression. Let Heroku handle it.
COLLECTFAST_ENABLED = False

# Use local filesystem for storage rather than Amazon S3.
DEFAULT_FILE_STORAGE    = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE     = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Set URLs to local ones.
MEDIA_ROOT         = root("..", "media")
STATIC_ROOT        = root("..", "static")
COMPRESS_ROOT      = root("..", "assets")
MEDIA_URL          = '/media/'
STATIC_URL         = '/static/'
COMPRESS_URL       = STATIC_URL
ADMIN_MEDIA_PREFIX = 'static/admin/'
COMPRESS_OFFLINE     = True

# IMPORTANT: set COMPRESS_ENABLED to True when compressing for deployment (with 'python manage.py compress').
COMPRESS_ENABLED     = False

# Host for our generated referral links.
REFERRAL_HOST = "localhost:8000"

# Properties for the local PostgreSQL database.
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'xavee_db',                      
        'USER': 'Kristian',
        'PASSWORD': 'kristian5634',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}