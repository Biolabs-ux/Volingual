# Backend/volingual/users/views/userdetail_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import CustomUser
from ..serializers.user_serializers import CustomUserSerializer


class UserDetailView(APIView):
    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            serializer = CustomUserSerializer(user)
            return Response(serializer.data, status=200)
        else:
            return Response({'status': 'error', 'message': 'User not found'}, status=404)
