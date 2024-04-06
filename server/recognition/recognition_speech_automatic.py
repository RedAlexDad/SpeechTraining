import os
from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RecognitionData, Metrics, Account

from rest_framework.permissions import AllowAny
from .permissions import IsModerator, get_access_token, get_jwt_payload
from .serializers import RecognitionDataSerializer, AccountSerializer, MetricsSerializer, \
    AccountAuthorizationSerializer, AccountSerializerInfo

import torch
import sounddevice as sd

# Для теста WER - Word Error Rate, CER - Character Error Rate, MER - Match Error Rate, WIL - Word Information Lost
from jiwer import wer, cer, mer, wil

# НЕ УБИРАЙТЕ ЭТУ ЯЧЕЙКУ, ИНАЧНЕ БУДЕТ НЕПРАВИЛЬНО ИНИЦИАЛИЗИРОВАНО ОКРУЖЕНИЕ, ЧТО И ВЫВЕДЕТ ОШИБКУ ВЕРСИИ ptxas!!!
os.environ['PATH'] = '/usr/local/cuda-12.3/bin:' + os.environ['PATH']

LANG_ID = 'ru'
MODEL_ID = 'bond005/wav2vec2-mbart50-ru'
PATH_MODEL = '/home/redalexdad/recognition_speech/wav2vec2-mbart50-ru'
device = 'cpu'

# Проверка доступности GPU
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Настройка количества процессоров и памяти
NUM_PROCESSES = max(1, os.cpu_count())
# print(f"Using device: {device}")

# Устанавливает максимальное количество доступной видеопамяти (например, 75%)
# torch.cuda.set_per_process_memory_fraction(0.75)
# Включает динамическое выделение памяти на GPU
# torch.cuda.set_per_process_memory_growth(True)

# Проверка наличия модели в локальном пути
if os.path.exists(PATH_MODEL):
    # Загрузка процессора из локального пути
    processor = Wav2Vec2Processor.from_pretrained(PATH_MODEL)

    # Загрузка модели из локального пути
    model = SpeechEncoderDecoderModel.from_pretrained(PATH_MODEL).to(device)
    print('Успешно модель загружена')
else:
    # Загрузка процессора из сети и сохранение в локальный путь
    processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
    processor.save_pretrained(PATH_MODEL)

    # Загрузка модели из сети и сохранение в локальный путь
    model = SpeechEncoderDecoderModel.from_pretrained(MODEL_ID).to(device)
    model.save_pretrained(PATH_MODEL)
    print(f'Успешно модель скачана и сохранена в пути {PATH_MODEL}')


class TranscriptionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    model_class = Account
    serializer_class = AccountSerializer

    def post(self, request, format=None):
        # Получим предложения из запроса
        sentences = request.data.get('sentences', None)
        reference_text = " ".join(sentence.lower() for sentence in sentences)
        # Запись голоса
        audio_data = self.record_audio()
        # Распознавание голоса
        transcription_text = self.transcribe_audio(audio_data, model, processor, device)

        print("Канонический текст:", reference_text)
        print("Распознанный текст:", transcription_text)

        # Проверяем на точность произношения
        wer_score, cer_score, mer_score, wil_score, iwer_score = self.calculate_metrics(reference_text, transcription_text)

        # Создаем объект метрики
        metrics = Metrics.objects.create(
            WER=wer_score,
            CER=cer_score,
            MER=mer_score,
            WIL=wil_score,
            IWER=iwer_score
        )

        account_serializer = self.get_info_account(request=request)

        # Сохраним транскрипцию в базе данных
        transcription = RecognitionData(
            text=transcription_text,
            transcription_text=transcription_text,
            data_recognition=audio_data,
            date_recoding=datetime.now().date(),
            id_metric=metrics.id,
            id_client=account_serializer.get('id') if account_serializer else None
        )
        transcription.save()

        transcription_serializer = RecognitionDataSerializer(transcription)
        metrics_serializer = MetricsSerializer(metrics)

        # Добавим данные метрики к данным транскрипции
        serialized_data = transcription_serializer.data
        serialized_data['metrics'] = metrics_serializer.data

        return Response(serialized_data, status=status.HTTP_201_CREATED)

    def get_info_account(self, request=None):
        error_message, access_token = get_access_token(request)

        if access_token is None:
            return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)
        payload = get_jwt_payload(access_token)
        account = Account.objects.filter(id=payload['id']).first()

        if account is None:
            return Response({'message': 'Такого аккаунта не найдено. Проверьте свои учетные данные'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Получение данных аккаунта
        account_serializer = AccountSerializerInfo(account, many=False).data

        return account_serializer

    # Функция записи голоса и возврата в виде массива для предсказания
    def record_audio(self, duration=3, sampling_rate=16000):
        print('Начало записи звука')
        recording = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=1, dtype='int16')
        sd.wait()
        print('Конец записи звука')
        return recording

    # Функция распознавания голоса, т.е. транскрибация
    def transcribe_audio(self, audio_data, model, processor, device):
        # Преобразование данных аудио в тензор
        audio_tensor = torch.FloatTensor(audio_data.squeeze()).to(device)

        # Предобработка данных
        processed = processor(audio_tensor, sampling_rate=16000, return_tensors="pt", padding='longest').to(device)
        try:
            with torch.no_grad():
                predicted_ids = model.generate(**processed).to(device)

                # Декодирование предсказаний
                transcription = processor.batch_decode(
                    predicted_ids,
                    num_processes=NUM_PROCESSES,
                    skip_special_tokens=True
                )[0]

                return transcription.lower()
        except Exception as error:
            print('ERROR: ', error)
            return error

    # Функция проверки всех метрик
    def calculate_metrics(self, reference_text, transcription_text):
        # Подсчет WER
        wer_score = wer(reference_text, transcription_text)
        # Подсчет CER
        cer_score = cer(reference_text, transcription_text)
        # Подсчет MER
        mer_score = mer(reference_text, transcription_text)
        # Подсчет WIL
        wil_score = wil(reference_text, transcription_text)
        # По
        iwer_score = 1 - self.iwer(reference_text, transcription_text)

        print(f"WER: {wer_score:.2f}, ", f"CER: {cer_score:.2f}, ", f"MER: {mer_score:.2f}, ",
              f"WIL: {wil_score:.2f}, ", f"IWER: {iwer_score:.2f};")

        return wer_score, cer_score, mer_score, wil_score, iwer_score

    def iwer(self, reference_sentence, hypothesis_sentence):
        """
        Вычисляет Inflectional Word Error Rate (IWER) между предложением-эталоном и гипотезой.

        Параметры:
        reference_sentence (str): Предложение-эталон (правильный вариант).
        hypothesis_sentence (str): Гипотеза (предсказанный вариант).

        Возвращает:
        float: Значение Inflectional Word Error Rate (IWER) в процентах.
        """
        reference_words = reference_sentence.split()
        hypothesis_words = hypothesis_sentence.split()

        # Находим количество слов в предложении-эталоне
        total_words = len(reference_words)

        # Считаем количество неправильно распознанных слов
        incorrect_words = sum(1 for ref, hyp in zip(reference_words, hypothesis_words) if ref != hyp)

        # Вычисляем Inflectional Word Error Rate (IWER)
        iwer_score = incorrect_words / total_words

        return iwer_score
