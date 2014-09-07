'''
Created on Jun 18, 2014

@author: Kristian
'''
from rest_framework import permissions, generics
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import WorldRanking, Application
from .serializers import ApplicationSerializer, IPhoneVersionSerializer, RankingSerializer

# API Mixins.
class ApplicationMixin(object):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
class VersionMixin(object):
    serializer_class = IPhoneVersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# API view classes.
class ApplicationList(ApplicationMixin, generics.ListAPIView):
    pass

class ApplicationRanking(generics.GenericAPIView):
    def get(self, request):
        country = request.GET.get('country')
        ranking_type = request.GET.get('ranking_type')
        category = request.GET.get('category')
        obj = None
        
        if category is None or int(category) <= 0:
            obj = get_object_or_404(WorldRanking, country=country, ranking_type=ranking_type, category=0)
        else:
            obj = get_object_or_404(WorldRanking, country=country, ranking_type=ranking_type, category=category)
            
        serializer = RankingSerializer(obj)
        return Response(serializer.data)
    
# class ApplicationVersionList(RankingMixin, generics.ListAPIView):
#     def get_queryset(self):
#         ranking_type = self.request.GET.get('ranking_type')
#         if ranking_type:
#             return WorldRanking.objects.filter(version__application__pk=self.kwargs.get('pk'), ranking_type=ranking_type)
#         else:
#             return WorldRanking.objects.filter(version__application__pk=self.kwargs.get('pk'))
        
class ApplicationDetail(ApplicationMixin, generics.RetrieveAPIView):
    pass

class VersionDetail(VersionMixin, generics.RetrieveAPIView):
    pass
