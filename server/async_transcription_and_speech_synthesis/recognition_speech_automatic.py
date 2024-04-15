import base64
import os
import time
import io
import numpy as np
import requests
from datetime import datetime

from django.db.models import Max, Count, F

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor

from rest_framework.response import Response
from rest_framework import status

from account.serializers import AccountSerializerInfo
from async_transcription_and_speech_synthesis.models import RecognitionData, DataRecognitionAndSynthesis

from rest_framework.permissions import AllowAny
from account.permissions import get_info_account
from async_transcription_and_speech_synthesis.serializers import RecognitionDataSerializer, DataRecognitionAndSynthesisSerializer

import torch
import sounddevice as sd
import soundfile as sf

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


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
# Отправка на запрос транскрибацию
def create_transcription(request, format=None):
    try:
        # Получаем аудиоданные из тела запроса
        audio_data = request.body

        # Преобразование байтов обратно в ndarray
        recording_restored = np.frombuffer(audio_data, dtype=np.int16)

        # Распознавание голоса
        start_time = time.time()
        transcription_text = transcribe_audio(recording_restored, model, processor, device)
        transcription_time = time.time() - start_time

        print("Время распознавания голоса:", transcription_time, "секунд")
        print("Распознанный текст:", transcription_text)

        return Response(data=transcription_text, status=status.HTTP_200_OK)
    except Exception as error:
        return Response(data={error.__class__.__name__: str(error)}, status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     # Преобразуем строку в объект Python JSON
    #     json_data = json.loads(request.body.decode('utf-8'))
    #     print(json_data)
    #     const_token = 'my_secret_token'
    #
    #     if const_token != json_data['token']:
    #         return Response(data={'message': 'Ошибка, токен не соответствует'}, status=status.HTTP_403_FORBIDDEN)
    #
    #     # Изменяем значение sequence_number
    #     try:
    #         # Выводит конкретную заявку создателя
    #         mars_station = get_object_or_404(MarsStation, pk=json_data['id_draft'])
    #         mars_station.status_mission = json_data['status_mission']
    #         # Сохраняем объект Location
    #         mars_station.save()
    #         data_json = {
    #             'id': mars_station.id,
    #             'status_task': mars_station.get_status_task_display_word(),
    #             'status_mission': mars_station.get_status_mission_display_word()
    #         }
    #         return Response(data={'message': 'Статус миссии успешно обновлен', 'data': data_json},
    #                         status=status.HTTP_200_OK)
    #     except ValueError:
    #         return Response({'message': 'Недопустимый формат преобразования'}, status=status.HTTP_400_BAD_REQUEST)
    # except json.JSONDecodeError as e:
    #     print(f'Error decoding JSON: {e}')
    #     return Response(data={'message': 'Ошибка декодирования JSON'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
# Начать транскрибацию
def start_transcription(request, format=None):
    # Получим предложения из запроса
    sentences = request.data.get('sentences', None)
    sentences = " ".join(sentence.lower() for sentence in sentences)
    transcription_text = ''
    # Запись голоса
    start_time = time.time()
    audio_data = record_audio(duration=1, sampling_rate=16000, channels=1)
    recording_time = time.time() - start_time

    print("Канонический текст:", sentences)
    print("Время записи голоса:", recording_time, "секунд")

    # Асинхронный веб-сервис
    url = 'http://127.0.0.1:8100/create_transcription/'
    try:
        # response = requests.put(url, data=audio_data, headers={'Content-Type': 'audio/wav'})
        response = requests.put(url, data=audio_data)
        print(f'response.status_code: {response.status_code}')
        print(f'response.text: {response.text}')
        transcription_text = response.text

        if response.status_code != 200:
            return Response(data=response.text, status=status.HTTP_400_BAD_REQUEST)
    except Exception as error:
        print(f'start_transcription; ERORR: {error}')

    # Проверяем на точность произношения
    wer_score, cer_score, mer_score, wil_score, iwer_score = calculate_metrics(sentences, transcription_text)

    # Сохраним транскрипцию в базе данных
    recognition_data = RecognitionData.objects.create(
        data_recognition=audio_data,
        transcription_word=transcription_text,
        word_for_check=sentences,
        date_recoding=datetime.now().date(),
        wer=wer_score,
        cer=cer_score,
        mer=mer_score,
        wil=wil_score,
        iwer=iwer_score
    )

    account_serializer = get_info_account(request=request)
    account_id = account_serializer['id'] if account_serializer is not None else None

    data = DataRecognitionAndSynthesis.objects.create(
        client_id=account_id,
        text_id=1,
        recognition_data_id=recognition_data.id,
        sequence_number=get_sequence_number(account_id)
    )

    recognition_data_serializer = RecognitionDataSerializer(recognition_data)
    data_serializer = DataRecognitionAndSynthesisSerializer(data)

    # Добавим данные метрики к данным транскрипции
    serialized_data = recognition_data_serializer.data

    return Response(data=serialized_data, status=status.HTTP_201_CREATED)

def get_sequence_number(account_id):
    # Определяем последний порядковый номер, если есть предыдущие записи
    last_sequence_number = DataRecognitionAndSynthesis.objects.aggregate(
        max_sequence_number=Max('sequence_number')
    )['max_sequence_number'] or 0

    # Определяем количество существующих записей для данного клиента
    existing_records_count = DataRecognitionAndSynthesis.objects.filter(
        client_id=account_id
    ).aggregate(
        records_count=Count('id')
    )['records_count']

    # Определяем порядковый номер
    sequence_number = last_sequence_number + 1 if existing_records_count else 1

    return sequence_number


def record_audio(duration=3, sampling_rate=16000, channels=1):
    try:
        print('Начало записи звука')
        recording = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=channels, dtype='int16')
        sd.wait()
        print('Конец записи звука')
        recording_bytes = recording.tobytes()

        # Сохраняем запись в формате WAV
        # with io.BytesIO() as wav_buffer:
        #     sf.write(wav_buffer, recording, samplerate=sampling_rate, format='WAV', subtype='PCM_16')
        #     wav_buffer.seek(0)
        #     wav_data = wav_buffer.read()

        return recording_bytes
    except Exception as error:
        print({error.__class__.__name__: str(error)})
        return None


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