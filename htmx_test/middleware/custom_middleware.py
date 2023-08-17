
from django.http import JsonResponse
from django.conf import settings
from htmx_test.config import thread_safe_lru_cache
from htmx_test.crypto import encrypt

from htmx_test.models import APIKey

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
            

        return self.get_response(request)
