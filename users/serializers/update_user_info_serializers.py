from rest_framework import serializers
from ..models import CustomUser


class UpdateUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'country')

    def validate(self, attrs):
        request_user = self.context['request'].user
        user_to_update = self.instance
        if request_user != user_to_update:
            raise serializers.ValidationError("You can only update your own information.")
        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance
