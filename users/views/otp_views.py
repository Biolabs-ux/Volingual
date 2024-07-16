# otp_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.otp_serializers import OTPVerificationSerializer
from ..models import CustomUser


class OTPVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp = serializer.validated_data.get('otp')
            user = CustomUser.objects.filter(email=email).first()
            if user and user.otp == otp:
                user.otp = None  # clear the otp
                user.save()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
