import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from django.contrib.auth import get_user_model
from chat.models import Message, Chat
from channels.layers import get_channel_layer

User = get_user_model()
channel_layer = get_channel_layer()

REDIS_ONLINE_USERS_KEY = "online_users"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            await self.add_online_user(self.user.id, self.user.email, self.user.username)

        self.room_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.remove_online_user(self.user.id, self.user.email, self.user.username)

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        try:
            user = await self.get_user(data["user"])
            chat = await self.get_chat(self.chat_id)
        except User.DoesNotExist:
            await self.send(text_data=json.dumps({"error": "Invalid user"}))
            return
        except Chat.DoesNotExist:
            await self.send(text_data=json.dumps({"error": "Invalid chat"}))
            return

        message = await self.create_message(user, chat, data["text"])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "user": user.username,
                "message": message.text,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "sender": event["user"],
            "message": event["message"],
        }))

    async def add_online_user(self, user_id, user_email, user_name):
        users = cache.get(REDIS_ONLINE_USERS_KEY, set())
        users.add((user_id, user_email, user_name))  # Store the entire user object
        cache.set(REDIS_ONLINE_USERS_KEY, users, timeout=None)
        await self.notify_admin_users()

    async def remove_online_user(self, user_id, user_email, user_name):
        users = cache.get(REDIS_ONLINE_USERS_KEY, set())
        users.discard((user_id, user_email, user_name))  # Remove the exact user object
        cache.set(REDIS_ONLINE_USERS_KEY, users, timeout=None)
        await self.notify_admin_users()

    async def notify_admin_users(self):
        users = self.get_online_users()
        formatted_users = [{"id": user[0], "email": user[1], "username": user[2]} for user in users]
        await self.channel_layer.group_send(
            "admin_updates",
            {
                "type": "update_admin",
                "users": formatted_users,
            }
        )

    @staticmethod
    def get_online_users():
        return cache.get(REDIS_ONLINE_USERS_KEY, set())

    @staticmethod
    async def get_user(user_id):
        return await User.objects.aget(id=user_id)

    @staticmethod
    async def get_chat(chat_id):
        return await Chat.objects.aget(id=chat_id)

    @staticmethod
    async def create_message(user, chat, text):
        return await Message.objects.acreate(user=user, chat=chat, text=text)


class AdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous or not self.user.is_staff:
            await self.close()
            return

        await self.channel_layer.group_add("admin_updates", self.channel_name)
        await self.accept()
        await self.send_online_users()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("admin_updates", self.channel_name)

    async def update_admin(self, event):
        await self.send(text_data=json.dumps({"online_users": event["users"]}))

    async def send_online_users(self):
        users = ChatConsumer.get_online_users()
        user_data = [{"id": user[0], "email": user[1], "username": user[2]} for user in users]
        await self.send(text_data=json.dumps({"online_users": user_data}))

