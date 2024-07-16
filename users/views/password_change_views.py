# password_change_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from ..models import CustomUser
from ..serializers.password_change_serializers import PasswordChangeSerializer


class PasswordChangeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            new_password = serializer.validated_data.get('new_password')
            user = CustomUser.objects.filter(email=email).first()
            if user:
                user.password = make_password(new_password)
                user.save()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
