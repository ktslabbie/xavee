'''
Created on May 18, 2014

@author: Kristian

The main URLConf for Xavee.
This contains URL routings to all apps and main pages (index, about, etc).
'''
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

from . import views
from blog.views import PostListView

# Generate the admin console for all models found.
admin.autodiscover()

# URL patterns: which URL requests route to which view.
urlpatterns = patterns('',
    url(r'^api/',       include('api.urls')),
    url(r'^api-auth/',  include('rest_framework.urls', namespace = 'rest_framework')),
    url(r'^blog/',      include('blog.urls',           namespace = 'blog')),

    url(r'^ckeditor/upload/', 'ckeditor.views.upload', name='ckeditor_upload'),
    url(r'^ckeditor/browse/', 'ckeditor.views.browse', name='ckeditor_browse'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/',     include(admin.site.urls)),
    url(r'^index/$',    views.HomepageView.as_view(),  name = 'home'),
    url(r'^about/$',    views.AboutView.as_view(),     name = 'about'),
    url(r'^$',          PostListView.as_view(),        name = 'post-list'),
)

# HTML5 Boilerplate patterns.
urlpatterns += patterns('',
    url(r'^apple-touch-icon\.png$', RedirectView.as_view(url='%simg/apple_icons/apple-touch-icon.png' % settings.STATIC_URL)),
    url(r'^crossdomain\.xml$',      TemplateView.as_view(template_name='html5/crossdomain.xml')),
    url(r'^favicon\.ico$',          RedirectView.as_view(url='%simg/favicon.ico' % settings.STATIC_URL)),
    url(r'^humans\.txt',            TemplateView.as_view(template_name='html5/humans.txt')),
    url(r'^robots\.txt',            TemplateView.as_view(template_name='html5/robots.txt')),
)

# If we're running locally, serve static files on the localhost rather than S3.
if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom 404 (not found) and 500 (error) pages.
handler404 = views.PageNotFoundView.as_view()
handler500 = views.ServerErrorView.as_view()
