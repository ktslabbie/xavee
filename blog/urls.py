'''
Created on May 18, 2014
@author: Kristian
'''
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.PostListMixin.as_view(), name = "post_list"),
    url(r'^(?P<slug>[\w\-]+)/$', views.PostDetailMixin.as_view(), name = "post_detail"),
)
