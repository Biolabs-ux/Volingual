# Backend/volingual/users/serializers/otp_serializers.py
from rest_framework import serializers


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
