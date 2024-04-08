import os

from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from gtts import gTTS
import io

from recognition.DB_Minio import DB_Minio


class SpeechSynthesisView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        minio = DB_Minio()

        # Получаем текст из запроса
        text = request.data.get('text', '')[0]
        print('text', text)

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

    def get(self, request):
        minio = DB_Minio()
        try:
            # Получаем аудиофайл из хранилища Minio
            audio_data = minio.get_object("trainer", "audio_file.mp3")

            # Отправляем аудиофайл как ответ с правильными заголовками
            response = HttpResponse(audio_data, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="speech.mp3"'
            response['Content-Length'] = len(audio_data)

            return response
        except Exception as ex:
            print(f'[ERROR] Не удалось получить аудиофайл из хранилища Minio: {ex}')
            return HttpResponse(status=500)
