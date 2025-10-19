"""
Custom middleware for handling 404 errors ONLY in DEBUG mode.
For production (DEBUG=False), Django's handler404 will be used automatically.
This ensures custom 404 page works on both development and production.
"""

from django.shortcuts import render
from django.http import Http404
from django.conf import settings


class Custom404Middleware:
    """
    Middleware to show custom 404 page when DEBUG=True (development only).
    On production (cse.neu.ac.bd, neu-cse.onrender.com), Django's handler404 
    in urls.py will handle 404 errors automatically when DEBUG=False.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """
        Handle Http404 exceptions ONLY when DEBUG=True (local development).
        When DEBUG=False (production), Django's handler404 takes over.
        """
        if isinstance(exception, Http404) and settings.DEBUG:
            return render(request, 'cse/404.html', status=404)
        return None
