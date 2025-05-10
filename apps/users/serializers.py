from rest_framework import serializers
from .models import TelegramVerification, User


class TelegramIDSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()


class VerificationCodeSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'telegram_id', 'phone_number', 'role']
