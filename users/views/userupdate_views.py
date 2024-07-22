from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.update_user_info_serializers import UpdateUserInfoSerializer
from ..models import CustomUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserUpdateView(GenericAPIView):
    serializer_class = UpdateUserInfoSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UpdateUserInfoSerializer,
        operation_id='Update User Info',
        responses={
            200: openapi.Response('User updated', UpdateUserInfoSerializer),
            400: 'Invalid data'
        }
    )
    def get_object(self):
        user_id = self.kwargs.get('pk')
        return CustomUser.objects.get(id=user_id)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            return Response({"error": "You do not have permission to update this user."}, status=403)
        serializer = self.get_serializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
