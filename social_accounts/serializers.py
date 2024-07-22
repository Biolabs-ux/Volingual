from rest_framework import serializers
from .utils import Google, register_social_user
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=5)

    def validate(self, access_token):
        google_user_data = Google.validate(access_token)
        try:
            userid = google_user_data["sub"]

        except:
            raise serializers.ValidationError("this token is invalid or has expired")

        if google_user_data["aud"] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed("this token is invalid")
        email = google_user_data["email"]
        first_name = google_user_data["given_name"]
        last_name = google_user_data["family_name"]
        country = google_user_data["country"]
        provider = "google"

        return register_social_user(provider, email, first_name, last_name, country)
