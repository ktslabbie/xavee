'''
Created on May 18, 2014
@author: Kristian
'''
from django.views.generic import TemplateView

class HomepageView(TemplateView):
    ''' Simple class-based view to render the Index page. '''
    template_name = "index.html"

class AboutView(TemplateView):
    ''' Simple class-based view to render the About page. '''
    template_name = "about.html"
