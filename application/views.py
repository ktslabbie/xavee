'''
Created on Oct 17, 2014

@author: Kristian
'''
from django.views.generic import TemplateView
from django.utils import translation
from django.shortcuts import render

class ApplicationTemplateView(TemplateView):
    ''' 
    The Application app routing is handled by AngularJS.
    Just return an index page that loads the necessary Angular resources. 
    '''
    template_name='application-index.html'
    
    def get(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return render(request, self.template_name)
        

    def get_context_data(self, **kwargs):
        context = super(ApplicationTemplateView, self).get_context_data(**kwargs)
        context['ANGULAR'] = True
        return context