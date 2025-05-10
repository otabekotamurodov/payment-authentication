from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'card_number', 'balance', 'created_at']
        read_only_fields = ['balance', 'created_at']
