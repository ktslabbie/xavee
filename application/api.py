'''
Created on Jun 18, 2014

@author: Kristian
'''
from rest_framework import permissions, generics
from .models import Application, Version, WorldRanking
from .serializers import ApplicationSerializer, VersionSerializer, RankingSerializer

# API Mixins.
class ApplicationMixin(object):
    model = Application
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
class VersionMixin(object):
    model = Version
    serializer_class = VersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
class RankingMixin(object):
    model = WorldRanking
    serializer_class = RankingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


# API view classes.
class ApplicationList(ApplicationMixin, generics.ListAPIView):
    pass

class ApplicationRanking(RankingMixin, generics.ListAPIView):
    def get_queryset(self):
        country = self.request.GET.get('country')
        ranking_type = self.request.GET.get('ranking_type')
        category = self.request.GET.get('category')
        if category <= 0: category = None
        return WorldRanking.objects.filter(country=country, ranking_type=ranking_type, category=category)
    
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
