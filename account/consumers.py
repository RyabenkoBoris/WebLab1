import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.consumers import ChatConsumer
from datetime import datetime

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

    async def send_operation_status(self, event):
        operation_status = {
            "result": event,
            "completion_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        await self.send(text_data=json.dumps({
            "operation_status": operation_status
        }))
