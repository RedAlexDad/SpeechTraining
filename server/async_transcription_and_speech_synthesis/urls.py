# urls.py для async_transcription_and_speech_synthesis
from django.urls import path
from async_transcription_and_speech_synthesis.recognition_speech_automatic import start_transcription, create_transcription
from async_transcription_and_speech_synthesis.speech_synthesis import create_speech_synthesis, test_speech_synthesis, get_speech_synthesis
from async_transcription_and_speech_synthesis.text import text, text_by_pk

urlpatterns = [
    # Получить запрос на транскрибацию
    path('start_transcription/', start_transcription, name='start_transcription'),
    # Начать транскрибацию
    path('create_transcription/', create_transcription, name='create_transcription'),
    # Создать синтез речи POST
    path('create_speech_synthesis/', create_speech_synthesis, name='create_speech_synthesis'),
    # Тест на прослушку POST
    path('test_speech_synthesis/', test_speech_synthesis, name='test_speech_synthesis'),
    # Получить существующий синтез речи GET
    path('repeat_speech_synthesis/', get_speech_synthesis, name='repeat_speech_synthesis'),
    # Получить список тем и текстов
    path('text/', text, name='text'),
    # Получить текст
    path('text/<int:pk>', text_by_pk, name='text_by_pk'),
]
