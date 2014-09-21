'''
Created on Aug 19, 2014
@author: Kristian
'''
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# URL patterns: which URL requests route to which view.
urlpatterns = patterns('',
    url(r'^$',                             TemplateView.as_view(template_name='application-list.html'),  name = 'application-list'),
    url(r'^(?P<pk>[0-9]+)',                TemplateView.as_view(template_name='application-detail.html'), name = "application-detail"),
    url(r'^/developers/(?P<pk>[0-9]+)',     TemplateView.as_view(template_name='developer-detail.html'), name = "developer-detail"),
    url(r'^/rankings$',                     TemplateView.as_view(template_name='application-ranking.html'), name = "application-ranking"),
)
