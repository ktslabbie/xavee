'''
Created on Jun 18, 2014

@author: Kristian
'''
from rest_framework import permissions, generics, filters
from django.shortcuts import get_object_or_404
from django.utils import translation
from rest_framework.response import Response
from .models import IPhoneVersion, Ranking, WorldRanking, Application, Developer
from .serializers import ApplicationSerializer, SimpleApplicationSerializer, IPhoneVersionSerializer, WorldRankingSerializer, DeveloperSerializer

# API Mixins.
class ApplicationMixin(object):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
class IPhoneVersionMixin(object):
    queryset = IPhoneVersion.objects.all()
    serializer_class = IPhoneVersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
class DeveloperMixin(object):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class ApplicationList(ApplicationMixin, generics.ListAPIView):
    serializer_class = SimpleApplicationSerializer
    
    def get_queryset(self):
        """
        This view should return a list of:
            if q, all tags that contain q
            else, all tags
        """
        queryset = Application.objects.all()
        query = self.request.QUERY_PARAMS.get('q', None)
        if query is not None:
            queryset = queryset.filter(title__istartswith=query)[:5]
        return queryset

class XaveeRanking(ApplicationMixin, generics.ListAPIView):
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('xavee_score', 'itunes_world_rating_count')
    ordering = ['-xavee_score', 'itunes_world_rating_count']
    
    def get_queryset(self):
        
        if self.kwargs['ranking_type'] == 'free':
            queryset = Application.objects.filter(categories__id=self.kwargs['category'], price=0.0)
        elif self.kwargs['ranking_type'] == 'paid':
            queryset = Application.objects.filter(categories__id=self.kwargs['category'], price__gt=0.0)
        else:
            queryset = Application.objects.filter(categories__id=self.kwargs['category'])
            
        return queryset

class ApplicationRanking(generics.GenericAPIView):
    def get(self, request, country, platform, ranking_type, category):
        translation.activate(request.LANGUAGE_CODE)
        
        if ranking_type == 'free':
            ranking_type = 1
        elif ranking_type == 'paid':
            ranking_type = 2
        elif ranking_type == 'grossing':
            ranking_type = 3
        
        obj = get_object_or_404(WorldRanking, country=country, ranking_type=ranking_type, category=category)
            
        serializer = WorldRankingSerializer(obj)
        return Response(serializer.data)
    
class ApplicationVersionList(IPhoneVersionMixin, generics.ListAPIView):
    def get_queryset(self):
        return Ranking.objects.filter(version__application__pk=self.kwargs.get('pk'))
        
class ApplicationDetail(ApplicationMixin, generics.RetrieveAPIView):
    pass

class VersionDetail(IPhoneVersionMixin, generics.RetrieveAPIView):
    pass

# API view classes.
class DeveloperList(DeveloperMixin, generics.ListAPIView):
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('xavee_score',)
    ordering = ['-xavee_score',]

class DeveloperDetail(DeveloperMixin, generics.RetrieveAPIView):
    pass
