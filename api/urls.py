'''
Created on Jun 18, 2014

@author: Kristian
'''
from django.conf.urls import patterns, url, include
from blog.api import PostList, PostDetail
from application.api import ApplicationList, ApplicationDetail, ApplicationRanking, DeveloperDetail
from . import views

# Additionally, we include the login URLs for the browseable API.
# user_urls = patterns('',
#     url(r'^/(?P<username>[0-9a-zA-Z_-]+)/posts/$',    UserPostList.as_view(), name='userpost-list'),
#     url(r'^/(?P<username>[0-9a-zA-Z_-]+)$',          UserDetail.as_view(),   name='user-detail'),
#     url(r'^$',                                       UserList.as_view(),     name='user-list'),
# )

post_urls = patterns('',
    url(r'^/(?P<slug>[\w\-]+)$',            PostDetail.as_view(),           name='post-detail'),
    url(r'^$',                              PostList.as_view(),             name='post-list'),
)

app_urls = patterns('',
    url(r'^/developers/(?P<pk>[0-9]+)/$',   DeveloperDetail.as_view(),      name='developer-detail'),
    url(r'^/rankings$',                     ApplicationRanking.as_view(),   name='application-ranking'),
    url(r'^/(?P<pk>[0-9]+)/$',              ApplicationDetail.as_view(),    name='application-detail'),
    url(r'^$',                              ApplicationList.as_view(),      name='application-list'),
)

urlpatterns = patterns('',
    url(r'/posts',  include(post_urls)),
    url(r'/apps',   include(app_urls)),
    url(r'^$',     views.APIRootView.as_view()),
)