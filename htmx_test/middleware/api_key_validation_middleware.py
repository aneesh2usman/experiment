
from django.http import JsonResponse
from django.conf import settings
from htmx_test.config import thread_safe_lru_cache
from htmx_test.crypto import encrypt

from htmx_test.models import APIKey

class APIKeyValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request URL matches the desired pattern
        if request.path.startswith('/api/v1/'):
            # print(request.META)
            api_key = request.META.get('HTTP_API_KEY')
            api_secret = request.META.get('HTTP_API_SECRET')
            # print("*******api_key***",api_key)
            # print("*******api_secret***",api_secret)
            # Check if the provided API key and secret are valid
            if not self.is_valid(api_key, api_secret):
                response_data = {'error': 'Invalid API key or secret'}
                return JsonResponse(response_data, status=403)

        return self.get_response(request)
    
    def is_valid(self, api_key, api_secret):
        try:
            if self.api_validation(api_key, api_secret):
                return True
            else:
                return False
        except APIKey.DoesNotExist:
            return False
    @thread_safe_lru_cache(maxsize=20)   
    def api_validation(self,api_key, api_secret):
        print("inside validation")
        # pp("encrypt api_key",encrypt(api_key))
        # pp("encrypt api_secret",encrypt(api_secret))
        return APIKey.objects.get(api_key=encrypt(api_key), api_secret=encrypt(api_secret))
        