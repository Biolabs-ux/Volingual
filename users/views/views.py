from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from ..serializers.user_serializers import CustomUserSerializer
from ..serializers.login_serializers import LoginSerializer
from rest_framework.response import Response
from ..utils import send_code_to_user
from ..models import OneTimePassword
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

class SignupUserView(GenericAPIView):
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        operation_description="This endpoint allows a user to sign up",
        responses={
            201: openapi.Response('User created', CustomUserSerializer),
            400: 'Invalid data',
        }
    )
    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_code_to_user(user['email'])
            #send email function user['email']
            return Response({
                'data': user,
                'message': f'Hello {user["first_name"]}, thanks for signing up. An email has been sent to {user["email"]} for verification.',
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmail(GenericAPIView):
    def post(self, request):
        otpcode = request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(otp=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({
                    'message': f'Hello {user.first_name}, your email has been verified.',
                }, status=status.HTTP_200_OK)
            return Response({
                'message': f'Hello {user.first_name}, your email has already been verified.',
            }, status=status.HTTP_204_NO_CONTENT)

        except OneTimePassword.DoesNotExist:
            return Response({
                'message': 'otp code not provided',
            }, status=status.HTTP_404_NOT_FOUND)

# class LoginUserView(GenericAPIView):
#     serializer_class = LoginSerializer
#     def post(self, request):
#         serializer=self.serializer
