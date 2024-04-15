import io
from jiwer import wer
from datetime import datetime
from gtts import gTTS

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from Web.DB_Minio import DB_Minio
from async_transcription_and_speech_synthesis.models import SynthesisData, DataRecognitionAndSynthesis
from account.permissions import get_info_account
from async_transcription_and_speech_synthesis.serializers import SynthesisDataSerializer


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def create_speech_synthesis(request):
    minio = DB_Minio()

    # Получаем текст из запроса
    text = request.data.get('text', '')
    text = " ".join(sentence.lower() for sentence in text)

    # Используем gTTS для синтеза речи из текста
    tts = gTTS(text=text, lang='ru')

    # Создаем буфер для хранения аудио данных
    audio_buffer = io.BytesIO()

    # Сохраняем аудио в буфер
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    # Получаем содержимое аудио буфера в виде байтов
    audio_data = audio_buffer.getvalue()

    # Получаем размер аудиофайла
    audio_length = len(audio_buffer.getvalue())

    # Записываем аудиофайл в хранилище Minio
    try:
        # Сохраняем аудиофайл в хранилище Minio
        minio.put_object("trainer", "audio_file.mp3", audio_data, audio_length, "audio/mpeg")
    except Exception as ex:
        print(f'[ERROR] Не удалось записать аудиофайл в хранилище Minio: {ex}')

    # Отправляем аудиофайл как ответ с правильными заголовками
    response = HttpResponse(audio_data, content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename="speech.mp3"'
    response['Content-Length'] = len(audio_data)

    return response


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def test_speech_synthesis(request):
    # Получаем текст из запроса
    word = request.data.get('word', '')
    word_input = request.data.get('word_input', '')
    word_input = " ".join(sentence.lower() for sentence in word_input)

    minio = DB_Minio()
    # Получаем аудиофайл из хранилища Minio
    audio_data = minio.get_object("trainer", "audio_file.mp3")

    # Сохраняем данные синтеза речи в базе данных
    synthesis_data = SynthesisData.objects.create(
        data_recognition=audio_data,
        word_synthesis=word,
        word_input=word_input,
        date_synthesis=datetime.now().date(),
        wer=wer(word_input, word),
    )

    account_serializer = get_info_account(request=request)

    DataRecognitionAndSynthesis.objects.create(
        id_client=account_serializer['id'] if account_serializer is not None else None,
        id_synthesis=synthesis_data.id,
    )

    synthesis_data_serialized = SynthesisDataSerializer(synthesis_data)

    return Response(synthesis_data_serialized.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def get_speech_synthesis(request):
    minio = DB_Minio()
    # Получаем аудиофайл из хранилища Minio
    audio_data = minio.get_object("trainer", "audio_file.mp3")
    # Отправляем аудиофайл как ответ с правильными заголовками
    response = HttpResponse(audio_data, content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename="speech.mp3"'
    response['Content-Length'] = len(audio_data)

    return response