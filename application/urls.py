'''
Created on Aug 19, 2014
@author: Kristian
'''
from django.conf.urls import patterns, url
from .views import ApplicationListView, ApplicationDetailView, ApplicationRankingView

# URL patterns: which URL requests route to which view.
urlpatterns = patterns('',
    url(r'^$',                  ApplicationListView.as_view(),  name = 'application-list'),
    url(r'^(?P<pk>[0-9]+)/',    ApplicationDetailView.as_view(), name = "application-detail"),
    url(r'^rankings/$',         ApplicationRankingView.as_view(), name = "application-ranking"),
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

