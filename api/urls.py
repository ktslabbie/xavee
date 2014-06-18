'''
Created on Jun 18, 2014

@author: Kristian
'''
from django.conf.urls import patterns, url, include
from blog.api import PostList, PostDetail, UserPostList
from . import views
from approduce.api import UserList, UserDetail

# Create a router and register our viewsets with it.
#router = DefaultRouter()
#router.register(r'posts', PostViewSet)
#router.register(r'users', UserViewSet)

# The API URLs are determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
user_urls = patterns('',
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/posts$',    UserPostList.as_view(), name='userpost-list'),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)$',          UserDetail.as_view(),   name='user-detail'),
    url(r'^$',                                       UserList.as_view(),     name='user-list'),
)

post_urls = patterns('',
    url(r'^/(?P<pk>\d+)$',                           PostDetail.as_view(),   name='post-detail'),
    url(r'^$',                                       PostList.as_view(),     name='post-list'),
)

urlpatterns = patterns('',
    url(r'users',  include(user_urls)),
    url(r'posts',  include(post_urls)),
    url(r'^$',     views.APIRootView.as_view()),
)