# Backend/volingual/users/serializers/forgot_pass_serializers.py
from rest_framework import serializers


class ForgotPassSerializer(serializers.Serializer):
    email = serializers.EmailField()
