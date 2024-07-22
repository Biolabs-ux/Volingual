# Backend/volingual/users/serializers/forgot_pass_serializers.py
from rest_framework import serializers
from ..models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes
from django.urls import reverse
from ..utils import send_normal_email


class ForgotPassSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    class Meta:
        fields = ['email']

        def validate(self, attrs):
            email = attrs.get('email')
            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                request = self.context.get('request')
                site_domain = get_current_site(request).domain
                relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
                abslink = f"http://{site_domain}{relative_link}"
                email_body = f"Hello, \n\nWe received a request to reset your password. Click the link below to reset your password. \n\n{abslink}"
                data = {
                    'email_body': email_body,
                    'email_subject': 'Reset your password',
                    'to_email': user.email

                }
                send_normal_email(data)
            return super().validate(attrs)
