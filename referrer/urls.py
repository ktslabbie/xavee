'''
Created on May 18, 2014
@author: Kristian
'''
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.redirect_to_store, name = "referral"),
)
