'''
Created on May 18, 2014

@author: Kristian
'''
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.HomepageView.as_view(), name = "referrer_home"),
    url(r'^', views.redirect, name="redirect"),
)

handler404 = "dh5bp.views.page_not_found"
handler500 = "dh5bp.views.server_error"