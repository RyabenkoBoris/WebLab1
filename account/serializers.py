from .models import User
from rest_framework import serializers
from django.core.validators import EmailValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "gender", "birth_date"]
        extra_kwargs = {
            'password': {"write_only": True, },}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


