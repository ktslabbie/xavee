'''
Created on Jun 8, 2014

@author: Kristian
'''
from rest_framework import serializers
from .models import Post
from xavee.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    # HyperlinkedRelatedField(view_name='user-detail', lookup_field='username')
    
    def get_validation_exclusions(self):
        exclusions = super(PostSerializer, self).get_validation_exclusions()
        return exclusions + ['author']
    
    class Meta:
        model = Post
        #fields = ('id', 'created_at', 'updated_at', 'title', 'slug', 'description', 'content', 'published', 'author',)
        #lookup_field = 'slug'
