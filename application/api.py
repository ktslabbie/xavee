'''
Created on Jun 18, 2014

@author: Kristian
'''
from rest_framework import permissions, generics
from django.shortcuts import get_object_or_404
from django.utils import translation
from rest_framework.response import Response
from .models import WorldRanking, Application, Developer
from .serializers import ApplicationSerializer, IPhoneVersionSerializer, RankingSerializer, DeveloperSerializer

# API Mixins.
class ApplicationMixin(object):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
class VersionMixin(object):
    serializer_class = IPhoneVersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
class DeveloperMixin(object):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


# API view classes.
class ApplicationList(ApplicationMixin, generics.ListAPIView):
    pass

class ApplicationRanking(generics.GenericAPIView):
    def get(self, request, country, platform, ranking_type, category):
        translation.activate(request.LANGUAGE_CODE)
        
        if ranking_type == "free":
            ranking_type = 1
        elif ranking_type == "paid":
            ranking_type = 2
        elif ranking_type == "grossing":
            ranking_type = 3
        
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

# API view classes.
class DeveloperList(DeveloperMixin, generics.ListAPIView):
    pass

class DeveloperDetail(DeveloperMixin, generics.RetrieveAPIView):
    pass
