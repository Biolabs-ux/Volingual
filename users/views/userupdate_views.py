# userupdate_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CustomUser
from ..serializers.user_serializers import CustomUserSerializer


class UserUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            if not request.data:  # Check if any data was provided in the request
                return Response({'status': 'error', 'message': 'No data provided for update'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = CustomUserSerializer(user, data=request.data,
                                              partial=True)  # Set partial=True to update a subset of the fields
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
