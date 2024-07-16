# user_delete_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from ..models import CustomUser
from ..serializers.user_delete_serializers import UserDeleteSerializer


class UserDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserDeleteSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = CustomUser.objects.filter(email=email).first()
            if user:
                if check_password(password, user.password):
                    user.delete()
                    return Response({'status': 'success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'message': 'Incorrect password'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
