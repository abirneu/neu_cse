"""
Custom middleware for handling 404 errors in DEBUG mode.
This allows showing custom 404 page even when DEBUG=True.
"""

from django.shortcuts import render
from django.http import Http404


class Custom404Middleware:
    """
    Middleware to show custom 404 page even when DEBUG=True.
    This catches Http404 exceptions and renders the custom 404 template.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """
        Handle Http404 exceptions and render custom 404 page.
        """
        if isinstance(exception, Http404):
            return render(request, 'cse/404.html', status=404)
        return None
