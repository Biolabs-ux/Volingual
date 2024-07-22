# Backend/volingual/users/serializers/user_serializers.py
from rest_framework import serializers
from ..models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'country', 'password']

        def validate(self, attrs):
            password = attrs.get('password', '')
            if len(password) < 8:
                raise serializers.ValidationError("Password must be at least 8 characters long")
            return attrs

        def create(self, validated_data):
            user = CustomUser.objects.create_user(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                country=validated_data['country'],
                password=validated_data['password']
            )
            return user

