'''
Created on May 18, 2014

@author: Kristian
'''
from django.conf.urls import patterns, url
from . import views
from xavee import views as main_views

urlpatterns = patterns('',
    url(r'^$', views.HomepageView.as_view(),         name = "referrer_home"),
    url(r'^',  views.redirect,                      name = "redirect"),
)

handler404 = main_views.PageNotFoundView.as_view()
handler500 = main_views.ServerErrorView.as_view()