# Backend/volingual/users/serializers/login_serializers.py
from rest_framework import serializers
from ..models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, min_length=6)
    password = serializers.CharField(max_length=100, write_only=True)
    first_name = serializers.CharField(max_length=100, read_only=True)
    last_name = serializers.CharField(max_length=100, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials try again")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        user_tokens = user.tokens()

        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh'))
        }
