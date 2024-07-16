# forgot_pass_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from ..models import CustomUser
from ..serializers.forgot_pass_serializers import ForgotPassSerializer
import random


class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPassSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = CustomUser.objects.filter(email=email).first()
            if user:
                otp = random.randint(100000, 999999)
                user.otp = otp  # assuming you have an otp field in your user model
                user.save()
                send_mail(
                    'Your OTP',
                    f'Your OTP is {otp}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Email not registered'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
