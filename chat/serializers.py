from rest_framework import serializers
from .models import Chat, Message, User

class AppInfoSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    logo = serializers.CharField()
    
class MessageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Message
        fields = ["id", "user", "chat", "text", "timestamp"]

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ["id", "name", "creator", "messages"]
        extra_kwargs = {"creator": {"read_only": True}, "timestamp": {"read_only": True}}

class AddUserToChatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Користувач не знайдений")
        return value