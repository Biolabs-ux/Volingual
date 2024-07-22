# forgot_pass_views.py
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from ..models import CustomUser
from ..serializers.forgot_pass_serializers import ForgotPassSerializer
from ..serializers.set_new_password_serializers import SetNewPasswordSerializer
import random
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PasswordResetView(GenericAPIView):
    serializer_class = ForgotPassSerializer

    @swagger_auto_schema(
        request_body=ForgotPassSerializer,
        operation_id='Password Reset',
        responses={
            200: openapi.Response('Success', ForgotPassSerializer),
            400: 'Invalid email'
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': "A link has been sent to your email"}, status=status.HTTP_200_OK)


class PasswordRestConfirm(GenericAPIView):

    @swagger_auto_schema(
        operation_id='Password Reset Confirm',
        responses={
            200: openapi.Response('Success', ForgotPassSerializer),
            400: 'Invalid email'
        }
    )
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'credentials are valid', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as e:
            return Response({'error': 'Token is not valid, please request a new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPassword(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    @swagger_auto_schema(
        request_body=SetNewPasswordSerializer,
        operation_id='Set New Password',
        responses={
            200: openapi.Response('Success', SetNewPasswordSerializer),
            400: 'Invalid email'
        }
    )
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password reset success'}, status=status.HTTP_200_OK)
