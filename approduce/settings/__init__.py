'''
Created on May 15, 2014

@author: Kristian
'''
from .base import *

try:
    from .local import *
except ImportError:
    pass

