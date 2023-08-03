from django.urls import path
from . import consumers
from django.urls import re_path 

websocket_urlpatterns = [
    re_path(r'ws/products/', consumers.ProductConsumer.as_asgi()),
    re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#     re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
# ]