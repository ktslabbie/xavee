'''
Created on May 31, 2014

@author: Kristian
'''
from django.conf import settings

def google_analytics(request):
    """
    Use the variable returned in this function to
    render the Google Analytics tracking code template.
    """
    ga_prop_id = getattr(settings, 'GA_CODE', False)
    
    if not settings.DEBUG and ga_prop_id:
        return { 'GA_CODE': ga_prop_id, }
    
    return {}