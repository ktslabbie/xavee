'''
Created on Oct 17, 2014

@author: Kristian
'''
from django.views.generic import TemplateView

class ApplicationTemplateView(TemplateView):
    template_name='application-index.html'

    def get_context_data(self, **kwargs):
        context = super(ApplicationTemplateView, self).get_context_data(**kwargs)
        context['ANGULAR'] = True
        return context