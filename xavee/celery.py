'''
Created on Jul 30, 2014

Main Celery file.

@author: Kristian
'''
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
 
# Instruct Celery to use the default Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xavee.settings')

# Create the app. 
app = Celery('xavee')

app.config_from_object('django.conf:settings')

# Tell Celery to autodiscover all tasks.py files in the app folders.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))