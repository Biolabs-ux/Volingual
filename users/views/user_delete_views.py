from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.user_delete_serializers import UserDeleteSerializer
from ..models import CustomUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserDeleteView(GenericAPIView):
    serializer_class = UserDeleteSerializer

    @swagger_auto_schema(
        request_body=UserDeleteSerializer,
        operation_id='Delete User',
        responses={
            204: openapi.Response('User deleted', UserDeleteSerializer),
            404: 'Email not found in our system. Enter a valid email.',
            400: 'Invalid email'
        }
    )
    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                user.delete()
                return Response({"message": f"The account tied to {email} has been deleted."},
                                status=status.HTTP_204_NO_CONTENT)
            except CustomUser.DoesNotExist:
                return Response({"message": "Email not found in our system. Enter a valid email."},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
