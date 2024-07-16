# signup_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from ..models import CustomUser
from ..serializers.signup_serializers import SignupSerializer


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            country = serializer.validated_data.get('country')
            user = CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password),
                country=country
            )
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
