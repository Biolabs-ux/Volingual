from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Translation
from ..serializers.translate_serializers import TranslationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TranslationHistoryAPIView(GenericAPIView):
    serializer_class = TranslationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='Get Translation History',
        responses={
            200: openapi.Response('Success', TranslationSerializer(many=True)),
            401: 'Authentication credentials were not provided'
        }
    )
    def get_queryset(self):
        # Filter translations by the current user
        return Translation.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
