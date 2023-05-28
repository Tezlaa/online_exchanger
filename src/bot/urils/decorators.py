import functools

from django.conf import settings
from django.http import Http404


def token_valid(func):
    """
    Checking for a valid token from the headers. Protection API

    Work if DEBUG=False!
    """
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if settings.DEBUG:
            return func(request, *args, **kwargs)
        
        try:
            token_api_request = args[0].headers['token']
        except KeyError:
            raise Http404
        
        if token_api_request != settings.TOKEN_API:
            raise Http404
        
        return func(request, *args, **kwargs)
    return wrapper