from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatMessage, ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope.get('user')

        # Reject anonymous connections
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Guard: ignore messages from unauthenticated users
        if not self.user or not self.user.is_authenticated:
            return

        data = json.loads(text_data)
        message = data.get('message', '').strip()
        chatRoomName = data.get('chatRoomName', self.room_name)

        if not message:
            return

        # Use the authenticated session user — never trust client-sent username
        username = self.user.username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chatRoomName': chatRoomName,
            }
        )
        await self.save_message(message, chatRoomName)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message':      event['message'],
            'username':     event['username'],
            'chatRoomName': event['chatRoomName'],
        }))

    @sync_to_async
    def save_message(self, message, chatRoomName):
        room = ChatRoom.objects.get(slug=chatRoomName)
        ChatMessage.objects.create(
            message=message,
            user=self.user,
            room=room,
        )
