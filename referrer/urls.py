'''
Created on May 18, 2014
@author: Kristian
'''
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',

    url(r'^(?P<origin>\w+)/(?P<app_title>\w+)/$', views.redirect_to_store,),
)
