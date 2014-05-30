'''
Created on May 15, 2014

@author: Kristian
'''
# Get the entire "base" settings file first.
from .base import *

# Try to import all methods from the local settings file...
try:
    from .local import *    # It worked. We are running locally so get the local settings as well.
except ImportError:
    pass                    # It failed. We are running remotely and don't need anything else.

