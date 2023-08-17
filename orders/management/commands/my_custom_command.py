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
from htmx_test.config import generate_api_key
from htmx_test.models import APIKey


from orders.models import Author, Book2, LineItem, LineItemImage,Order
from datetime import date
def get_product_list():
    products = Author.objects.all()
    product_list = [{'id': product.id, 'name': product.name} for product in products]
    return product_list


class Command(BaseCommand):
    help = 'My custom command that does something.'

    def handle(self, *args, **kwargs):
        # Your code here
        # For example:
        # lineitems2 = LineItem.objects.all().select_related("order","lineitemimage").values(
        #         "name","order__name","lineitemimage__name"
        #     )
        
        # print(lineitems2)

        # asd = LineItemImage.objects.all().select_related("lineitem").values(
        #         "name","lineitem__name","lineitem__order__name"
        #     )
        
        # print(asd)

        # orders = Order.objects.prefetch_related("lineitem_set").all()

        # for order in orders:
        #     print(order.lineitem_set.all())
        #     print(order.lineitem_set.all().query)

        # api_key = APIKey(
        #     api_key=generate_api_key(length=32),
        #     api_secret=generate_api_key(length=64)
        # )
        # print(api_key.__dict__)
        # api_key.save()
        # print(api_key.__dict__)
        # print(api_key._api_key)
        # print(api_key._api_secret)
        from faker import Faker

        fake = Faker()

        # Generate a random name
        random_name = fake.name()
        print(random_name)

        # Generate a random address
        random_address = fake.address()
        print(random_address)
        print(fake.vin())
   


        
       
