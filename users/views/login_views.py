# login_views.py
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from ..serializers.login_serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication


class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_id='User Login',
        responses={
            200: openapi.Response('Success', LoginSerializer),
            400: 'Invalid login credentials'
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            'message': 'You are authenticated'
        }
        return Response(data, status=status.HTTP_200_OK)
