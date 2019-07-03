# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer

import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'message': message,
                    'user': self.user_name
                }
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': self.user_name
        }))

class PrivatChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_name = self.scope['url_route']['kwargs']['user_name']

        self.from_to = 'chat_%s' % (self.user_name + self.room_name)

        # Join room group

        await self.channel_layer.group_add(
            self.from_to,
            self.channel_name

        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.from_to,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        to_from = 'chat_%s' % (str(text_data_json['to']) + self.room_name)
        await self.channel_layer.group_send(
            to_from,
            {
                'type': 'chat_message',
                'message': {
                    'message': message,
                    'from': self.user_name,
                    'to': str(text_data_json['to'])
                }
            }
        )

        await self.channel_layer.group_send(
            self.from_to,
            {
                'type': 'chat_message',
                'message': {
                    'message': message,
                    'from': self.user_name,
                    'to': str(text_data_json['to'])
                }
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

