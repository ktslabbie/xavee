'''
Created on May 18, 2014

@author: Kristian
'''
#from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import UserSerializer

#class HomepageView(TemplateView):
#    ''' Simple class-based view to render the Index page. '''
#    template_name = "index.html"

#class AboutView(TemplateView):
#    ''' Simple class-based view to render the About page. '''
#    template_name = "about.html"

class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    lookup_field = 'username'