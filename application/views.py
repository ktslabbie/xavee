from django.views.generic import ListView, DetailView
from .models import Application, WorldRanking

class ApplicationMixin(object):
    model = Application

class RankingMixin(object):
    model = WorldRanking

class ApplicationListView(ApplicationMixin, ListView):
    pass
 
class ApplicationDetailView(ApplicationMixin, DetailView):
    pass

class ApplicationRankingView(RankingMixin, ListView):
    pass
