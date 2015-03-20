'''
Created on Aug 10, 2014

@author: Kristian
'''
import sys, time

"""
Helper to get an object from the DB, or None if it doesn't exists.
Django's standard get() function gives an exception in this case.
"""
def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    
"""
Get an app or developer slug from an iTunes URL.
This is easier than dealing with slug generation ourselves.
"""
def get_slug_from_itunes_url(url):
    url_parts = url.split('/')
    for i in range(0, len(url_parts)):
        if url_parts[i] == "artist" or url_parts[i] == "app":
            return url_parts[i+1]
        
""" 
Retry loop. Useful for remote API calling over an uncertain network.

Usage:

for retry in retryloop(10, timeout=30):
    try:
        something
    except SomeException:
        retry()

for retry in retryloop(10, timeout=30):
    something
    if somecondition:
        retry()

"""
class RetryError(Exception):
    pass

def retryloop(attempts, timeout=None, delay=0, backoff=1):
    starttime = time.time()
    success = set()
    for i in range(attempts): 
        success.add(True)
        yield success.clear
        if success:
            return
        duration = time.time() - starttime
        if timeout is not None and duration > timeout:
            break
        if delay:
            time.sleep(delay)
            delay = delay * backoff

    e = sys.exc_info()[1]

    # No pending exception? Make one
    if e is None:
        try: raise RetryError
        except RetryError as e: pass

    # Decorate exception with retry information:
    e.args = e.args + ("on attempt {0} of {1} after {2:.3f} seconds".format(i, attempts + 1, duration),)

    raise