import functools

from django.shortcuts import get_object_or_404

from apps.trade.models import OpenOrder


def valid_open_order(id_in_link: bool = True):
    """Check on open order in the database

    Args:
        id_in_link (bool, optional): If id_order is not in the link.
            Defaults to False.
    """
    
    def decorator(func):
        
        @functools.wraps(func)
        def wrapper(*args, **kwarks):
            if not id_in_link:
                id_order = args[1].GET['id_order']
            else:
                id_order = kwarks.get('id_order')

            object_database = get_object_or_404(OpenOrder, order__id_order=id_order)
            if id_in_link:
                kwarks['object_database'] = object_database
                
            return func(*args, **kwarks)
        return wrapper
    return decorator