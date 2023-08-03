import json
from django.core.management.base import BaseCommand
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


from orders.models import Author, Book2

def get_product_list():
    products = Author.objects.all()
    product_list = [{'id': product.id, 'name': product.name} for product in products]
    return product_list
class Command(BaseCommand):
    help = 'My custom command that does something.'

    def handle(self, *args, **kwargs):
        # Your code here
        # For example:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "product_list",
            {
                "type": "update_product_list",
                "message": "A new product has been added."
            }
        )

        
       
