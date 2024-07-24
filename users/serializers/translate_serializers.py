from rest_framework import serializers
from ..models import Translation


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['id', 'input_text', 'translated_text', 'created_at', 'user']
        read_only_fields = ('user', 'created_at')

    def create(self, validated_data):
        # Ensure the request object is available in the serializer context
        request = self.context.get('request', None)
        if request and hasattr(request, 'user'):
            # Assign the authenticated user to the 'user' field
            validated_data['user'] = request.user
        else:
            # Handle cases where the request or user is not available
            raise serializers.ValidationError("User must be authenticated to perform this action.")
        return super().create(validated_data)
