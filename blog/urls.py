'''
Created on May 18, 2014
@author: Kristian
'''
from django.conf.urls import patterns, url
from .views import PostListView, PostDetailView

# URL patterns: which URL requests route to which view.
urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(),  name = 'post-list'),
    url(r'^(?P<slug>[\w\-]+)/$',    PostDetailView.as_view(), name = "post-detail"),
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

