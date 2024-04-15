# urls.py для async_transcription_and_speech_synthesis
from django.urls import path
from async_transcription_and_speech_synthesis.recognition_speech_automatic import transcription
from async_transcription_and_speech_synthesis.speech_synthesis import create_speech_synthesis, test_speech_synthesis, get_speech_synthesis

urlpatterns = [
    # Транскрибация
    path('transcribe/', transcription, name='transcription'),
    # Создать синтез речи POST
    path('create_speech_synthesis/', create_speech_synthesis, name='create_speech_synthesis'),
    # Тест на прослушку POST
    path('test_speech_synthesis/', test_speech_synthesis, name='test_speech_synthesis'),
    # Получить существующий синтез речи GET
    path('repeat_speech_synthesis/', get_speech_synthesis, name='repeat_speech_synthesis'),
]
