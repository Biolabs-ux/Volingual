# Backend/volingual/users/serializers/user_delete_serializers.py
from rest_framework import serializers


class UserDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
