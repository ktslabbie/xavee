'''
Created on May 18, 2014

@author: Kristian
'''
#from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer

class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    lookup_field = 'username'