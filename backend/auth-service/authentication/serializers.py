from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_verified')
        read_only_fields = ('id', 'is_verified')

class SocialAuthSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=50)
    access_token = serializers.CharField()