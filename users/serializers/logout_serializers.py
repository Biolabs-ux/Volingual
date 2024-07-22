# Backend/volingual/users/serializers/otp_serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is invalid or expired'
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
