import json

class JSONMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ('POST', 'PUT', 'PATCH') and request.content_type == 'application/json':
            try:
                request.data = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                pass
        
        response = self.get_response(request)
        return response