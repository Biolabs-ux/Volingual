# Backend/volingual/users/serializers/password_change_serializers.py
from rest_framework import serializers
from django.utils.encoding import smart_str, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed

from ..models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            if password != confirm_password:
                raise AuthenticationFailed("Passwords do not match")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
# Backend/volingual/users/serializers/user_serializers.py
