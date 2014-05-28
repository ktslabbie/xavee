'''
Created on May 28, 2014

Module with some custom-made utility functions.

@author: Kristian
'''
import urllib
from django.core.urlresolvers import reverse

# Build a URL with GET parameters.
def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, **kwargs)
    if get:
        url += '?' + urllib.parse.urlencode(get)
    return url