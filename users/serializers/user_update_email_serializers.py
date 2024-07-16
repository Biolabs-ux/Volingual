# Backend/volingual/users/serializers/user_update_email_serializers.py
from rest_framework import serializers


class UserUpdateEmailSerializer(serializers.Serializer):
    current_email = serializers.EmailField()
    new_email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
