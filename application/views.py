from django.views.generic import ListView, DetailView
from .models import Application, Ranking

class ApplicationMixin(object):
    model = Application

class RankingMixin(object):
    model = Ranking

class ApplicationListView(ApplicationMixin, ListView):
    pass
 
class ApplicationDetailView(ApplicationMixin, DetailView):
    pass

class ApplicationRankingView(RankingMixin, ListView):
    pass
