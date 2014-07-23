'''
Created on Jun 18, 2014

@author: Kristian
'''
from rest_framework import permissions, generics
from .models import Post
from .serializers import PostSerializer

class PostMixin(object):
    model = Post
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def get_queryset(self):
        return self.model.objects.live()
    
    def pre_save(self, obj):
        ''' Force author to current user on save. '''
        obj.author = self.request.user
        return super(PostMixin, self).pre_save(obj)


class PostList(PostMixin, generics.ListCreateAPIView):
    pass


class PostDetail(PostMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'


class UserPostList(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer
    
    def get_queryset(self):
        queryset = super(UserPostList, self).get_queryset()
        return queryset.filter(author__username=self.kwargs.get('username'))

