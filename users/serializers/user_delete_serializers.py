from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from ..models import CustomUser


class UserDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField()

    @staticmethod
    def validate_email(email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return email
