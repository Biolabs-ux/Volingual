from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.user_info_serializers import UserInfoSerializer
from ..models import CustomUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    @swagger_auto_schema(
        operation_id='Get User Info',
        responses={
            200: openapi.Response('User Info', UserInfoSerializer),
            404: 'User not found'
        }
    )
    def get_object(self):
        return self.request.user
