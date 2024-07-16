# login_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from ..serializers.login_serializers import LoginSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                user_data = self.serialize_user(user)

                return Response({'status': 'success', 'data': user_data}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Invalid login credentials'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def serialize_user(self, user):
        # Convert the CustomUser object into a dictionary
        return {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'country': user.country,
            # Include any other fields you wish to return
        }