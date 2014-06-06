'''
Created on May 18, 2014
@author: Kristian
'''
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from filebrowser.sites import site
from dh5bp.urls import urlpatterns as dh5bp_urls
from . import views

# Generate the admin console for all models found.
admin.autodiscover()

# URL patterns: which URL requests route to which view.
urlpatterns = patterns('',
    url(r'^$',                  views.HomepageView.as_view(), name = "home"),
    url(r'^blog/',              include("blog.urls", namespace = "blog")),
    url(r'^about/$',            views.AboutView.as_view(),    name = "about"),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/',         include('grappelli.urls')), # grappelli URLs
    url(r'^admin/',             include(admin.site.urls)),
    
    url(r'^static/(.*)$',   'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
    
    #url(r'^media/(.*)$', 'django.views.static.serve', {
    #    'document_root': settings.MEDIA_ROOT,
    #}),
)

# Add the HTML5 Boilerplate URLs.
urlpatterns += dh5bp_urls

# Custom 404 (not found) and 500 (error) pages.
handler404 = "dh5bp.views.page_not_found"
handler500 = "dh5bp.views.server_error"