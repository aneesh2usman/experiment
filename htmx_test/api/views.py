import json
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict

from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from htmx_test.models import SampleImage
csrf_exempt_view = method_decorator(csrf_exempt, name='dispatch')


class ApiValidationView(View):
    @csrf_exempt_view
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        data={}
        return JsonResponse(data, safe=False)
    

class ApiImageView(View):
    @csrf_exempt_view
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        # image = SampleImage()
        # # image.image = request.data["image"]
        # image.create_from_base64(request.data["image"])
        # # print(image.image)
        # image.save()
        asd = {
            "image1":request.data["image"],
            "image2":request.data["image"],
            "image3":request.data["image"],
            "image4":request.data["image"],
            "image5":request.data["image"],
            "image6":request.data["image"],
            }
        asd = {
            "image1":"asd sdddv asd sddsd asd dd ffggf ggh gh gh ghghh gh hghg  hg ghh"
            }
        return JsonResponse(asd, safe=False)