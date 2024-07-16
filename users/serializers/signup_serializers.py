# Backend/volingual/users/serializers/signup_serializers.py
from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    country = serializers.CharField(max_length=50)
