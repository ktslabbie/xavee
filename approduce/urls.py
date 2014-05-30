from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from dh5bp.urls import urlpatterns as dh5bp_urls
from . import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.HomepageView.as_view(), name = "home"),
    url(r'^blog/', include("blog.urls", namespace = "blog")),
    url(r'^admin/tinymce/', include('tinymce.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT
    }),
)

urlpatterns += dh5bp_urls

handler404 = "dh5bp.views.page_not_found"
handler500 = "dh5bp.views.server_error"