from rest_framework import serializers
from .models import User , Item

class UserSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'items']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

class ItemSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Item
        fields = ['id', 'item_text', 'user']


