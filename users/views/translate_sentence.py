from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from ..models import Translation
from ..serializers.translate_serializers import TranslationSerializer
from ..text_translation.translate import translate_sentence, read_sentences
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

english_sentences = read_sentences('users/text_translation/data/english_sentences.txt')
nweh_sentences = read_sentences('users/text_translation/data/nweh_sentences.txt')


class TranslationAPIView(GenericAPIView):
    serializer_class = TranslationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=TranslationSerializer,
        operation_id='Translate Sentence',
        responses={
            201: openapi.Response('Success', TranslationSerializer),
            400: 'Invalid input'
        }
    )
    def post(self, request, *args, **kwargs):
        input_text = request.data.get('input_text')
        if not input_text:
            return Response({'error': 'No input text provided'}, status=status.HTTP_400_BAD_REQUEST)

        translated_text = translate_sentence(input_text, english_sentences, nweh_sentences)
        # Check if the user is authenticated and get the user's ID
        user_id = request.user.id if request.user.is_authenticated else None

        # Prepare data for serialization with user's ID if available
        data = {
            'user': user_id,
            'input_text': input_text,
            'translated_text': translated_text
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

