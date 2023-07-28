from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/product_list/', consumers.ProductListConsumer.as_asgi()),
]