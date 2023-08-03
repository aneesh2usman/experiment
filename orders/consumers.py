import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# class ProductConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Perform any necessary connection tasks here
#         self.room_group_name = 'testeee'

#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Perform any necessary disconnection tasks here
#         pass

#     async def update_product_list(self, event):
#         # This method will be called when a product list update event is received
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
class ProductConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "product_list"
        # Add the user to the WebSocket group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the WebSocket group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def update_product_list(self, event):
        # Send the product list update to the client
        await self.send(text_data=json.dumps({
            'type':'get_product_list',
            'message': event['message']
        }))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))