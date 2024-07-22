# logout_views.py
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.logout_serializers import LogoutUserSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LogoutUserSerializer,
        operation_id='Logout User',
        responses={
            204: openapi.Response('User logged out', LogoutUserSerializer),
            400: 'Invalid email'
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
