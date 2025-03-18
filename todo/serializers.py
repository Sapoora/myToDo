from rest_framework import serializers
from .models import User , Item

class UserSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'items']

class ItemSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Item
        fields = ['id', 'item_text', 'user']


