'''
Created on May 18, 2014
@author: Kristian
'''
from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"