'''
Created on Jul 15, 2014

@author: Kristian
'''
from django import template

register = template.Library()

@register.simple_tag
def active_page(request, view_names):
    from django.core.urlresolvers import resolve, Resolver404
    if not request:
        return ""
    try:
        for view_name in view_names:
            return "active" if resolve(request.path_info).url_name.startswith(view_name) else ""
    except Resolver404:
        return ""