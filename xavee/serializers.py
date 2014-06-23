'''
Created on Jun 8, 2014

@author: Kristian
'''
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(many=True, slug_field='slug')
    #posts = PostSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'posts',)
        lookup_field = 'username'