'''
Created on May 18, 2014

@author: Kristian

The main URLConf for Xavee.
This contains URL routings to all apps and main pages (index, about, etc).
'''
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.i18n import i18n_patterns

# Generate the admin console for all models found.
admin.autodiscover()

# URL patterns: which URL requests route to which view.
urlpatterns = patterns('',
    url(r'^api',                   include('api.urls')),
    url(r'^api-auth',              include('rest_framework.urls',                      namespace='rest_framework')),

    url(r'^ckeditor/upload/',       'ckeditor.views.upload',                            name='ckeditor_upload'),
    url(r'^ckeditor/browse/',       'ckeditor.views.browse',                            name='ckeditor_browse'),
    url(r'^grappelli/',             include('grappelli.urls')),
    url(r'^admin/',                 include(admin.site.urls)),
    url(r'^i18n/',                  include('django.conf.urls.i18n')),
)

urlpatterns += i18n_patterns('',
    url(r'^blog',                  include('blog.urls',                                namespace='blog')),
    url(r'^apps',                  include('application.urls',                         namespace='application')),
    url(r'^about$',                TemplateView.as_view(template_name='about.html'),   name='about'),
    #url(r'^$',                     TemplateView.as_view(template_name='index.html'),   name='home'),
    url(r'^$',                     RedirectView.as_view(url='apps'),                   name='home'),
)

# HTML5 Boilerplate patterns.
urlpatterns += patterns('',
    url(r'^apple-touch-icon\.png$', RedirectView.as_view(url='%simg/apple_icons/apple-touch-icon.png' % settings.STATIC_URL)),
    url(r'^crossdomain\.xml$',      TemplateView.as_view(template_name='html5/crossdomain.xml')),
    url(r'^favicon\.ico$',          RedirectView.as_view(url='%simg/favicon.ico' % settings.STATIC_URL)),
    url(r'^humans\.txt$',            TemplateView.as_view(template_name='html5/humans.txt')),
    url(r'^robots\.txt$',            TemplateView.as_view(template_name='html5/robots.txt')),
)

# If we're running locally, serve static files on the localhost rather than S3.
if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

