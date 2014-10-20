'''
Created on Aug 19, 2014
@author: Kristian
'''
from django.conf.urls import patterns, url
from views import ApplicationTemplateView

# URL patterns: which URL requests route to which view.
urlpatterns = patterns('',
    url(r'^',                             ApplicationTemplateView.as_view(), name = "application-index"),
)
