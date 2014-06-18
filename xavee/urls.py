'''
Created on May 18, 2014
@author: Kristian
'''
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
#from filebrowser.sites import site
from . import views
from blog.views import PostListView
from dh5bp.urls import urlpatterns as dh5bp_urls

# Generate the admin console for all models found.
admin.autodiscover()


# URL patterns: which URL requests route to which view.
urlpatterns = patterns('',
    url(r'^api/',               include('api.urls')),
    url(r'^api-auth/',          include('rest_framework.urls',  namespace = 'rest_framework')),
    url(r'^blog/',              include('blog.urls',            namespace = 'blog')),
#    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/',         include('grappelli.urls')),
    url(r'^admin/',             include(admin.site.urls)),
    
    url(r'^static/(.*)$',   'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
                       
    url(r'^index/$',     views.HomepageView.as_view(),   name = 'home'),
    url(r'^$',          PostListView.as_view(),   name = 'post-list'),
    url(r'^about/$',    views.AboutView.as_view(),      name = 'about'),
)

# Add the HTML5 Boilerplate URLs.
urlpatterns += dh5bp_urls

# Custom 404 (not found) and 500 (error) pages.
handler404 = "dh5bp.views.page_not_found"
handler500 = "dh5bp.views.server_error"