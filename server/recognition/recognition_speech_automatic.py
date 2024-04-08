import os
from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Account, RecognitionData, DataRecognitionAndSynthesis

from rest_framework.permissions import AllowAny
from .permissions import IsModerator, get_access_token, get_jwt_payload, get_info_account
from .serializers import RecognitionDataSerializer, AccountSerializer, \
    AccountAuthorizationSerializer, AccountSerializerInfo, DataRecognitionAndSynthesisSerializer

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


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def transcription(request, format=None):
    # Получим предложения из запроса
    sentences = request.data.get('sentences', None)
    sentences = " ".join(sentence.lower() for sentence in sentences)
    flag_synthesis = request.data.get('flag_synthesis', False)

    # Запись голоса
    audio_data = record_audio(duration=3, sampling_rate=16000, channels=1)
    # Распознавание голоса
    transcription_text = transcribe_audio(audio_data, model, processor, device)

    print("Канонический текст:", sentences)
    print("Распознанный текст:", transcription_text)

    # Проверяем на точность произношения
    wer_score, cer_score, mer_score, wil_score, iwer_score = calculate_metrics(sentences, transcription_text)

    # Сохраним транскрипцию в базе данных
    recognition_data = RecognitionData.objects.create(
        data_recognition=audio_data,
        transcription_text=transcription_text,
        text_for_check=sentences,
        date_recoding=datetime.now().date(),
        wer=wer_score,
        cer=cer_score,
        mer=mer_score,
        wil=wil_score,
        iwer=iwer_score
    )

    account_serializer = get_info_account(request=request)

    data = DataRecognitionAndSynthesis.objects.create(
        id_client=account_serializer['id'] if account_serializer is not None else None,
        id_recognition=recognition_data.id,
    )

    recognition_data_serializer = RecognitionDataSerializer(recognition_data)
    data_serializer = DataRecognitionAndSynthesisSerializer(data)

    # Добавим данные метрики к данным транскрипции
    serialized_data = recognition_data_serializer.data

    return Response(serialized_data, status=status.HTTP_201_CREATED)


def record_audio(duration=3, sampling_rate=16000, channels=1):
    print('Начало записи звука')
    recording = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=channels, dtype='int16')
    sd.wait()
    print('Конец записи звука')
    return recording


def transcribe_audio(audio_data, model, processor, device):
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
def calculate_metrics(reference_text, transcription_text):
    # Подсчет WER
    wer_score = wer(reference_text, transcription_text)
    # Подсчет CER
    cer_score = cer(reference_text, transcription_text)
    # Подсчет MER
    mer_score = mer(reference_text, transcription_text)
    # Подсчет WIL
    wil_score = wil(reference_text, transcription_text)
    # По
    iwer_score = 1 - iwer(reference_text, transcription_text)

    print(f"WER: {wer_score:.2f}, ", f"CER: {cer_score:.2f}, ", f"MER: {mer_score:.2f}, ",
          f"WIL: {wil_score:.2f}, ", f"IWER: {iwer_score:.2f};")

    return wer_score, cer_score, mer_score, wil_score, iwer_score


def iwer(reference_sentence, hypothesis_sentence):
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