from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from async_transcription_and_speech_synthesis.models import DataRecognitionAndSynthesis, Text
from async_transcription_and_speech_synthesis.serializers import TextSerializer


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def texts(request):
    texts = Text.objects.all()
    serializer = TextSerializer(texts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def text_by_pk(request, pk):
    try:
        data = DataRecognitionAndSynthesis.objects.get(pk=pk)
        text = data.text
        serializer = TextSerializer(text)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except DataRecognitionAndSynthesis.DoesNotExist:
        return Response({'error': 'Текст не найден'}, status=status.HTTP_404_NOT_FOUND)
