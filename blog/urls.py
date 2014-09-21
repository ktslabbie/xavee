'''
Created on May 18, 2014
@author: Kristian
'''
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

# URL patterns: which URL requests route to which view.
urlpatterns = patterns('',
    url(r'^$',                      TemplateView.as_view(template_name='post-list.html'),  name = 'post-list'),
    url(r'^(?P<slug>[\w\-]+)/$',    TemplateView.as_view(template_name='post-detail.html'),  name = 'post-detail'),
)

# 
# urlpatterns = patterns('',
#     url(r'^$',                           'blog.views.api_root',                  ),
#     url(r'^posts/$',                      views.PostList.as_view(),   name = "post-list"),
#     url(r'^posts/(?P<slug>[\w\-]+)/$',    views.PostDetail.as_view(), name = "post-detail"),
#     url(r'^users/$',                      views.UserList.as_view(),   name = "user-list"),
#     url(r'^users/(?P<pk>[0-9]+)/$',       views.UserDetail.as_view(), name = "user-detail"),
# )
# 
# urlpatterns = format_suffix_patterns(urlpatterns)

