import os

from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transcription
from .serializers import TranscriptionSerializer

import torch
import sounddevice as sd

# Для теста WER - Word Error Rate
# CER - Character Error Rate
# MER - Match Error Rate
# WIL - Word Information Lost
from jiwer import wer, cer, mer, wil

from Web.settings import BASE_DIR

# НЕ УБИРАЙТЕ ЭТУ ЯЧЕЙКУ, ИНАЧНЕ БУДЕТ НЕПРАВИЛЬНО ИНИЦИАЛИЗИРОВАНО ОКРУЖЕНИЕ, ЧТО И ВЫВЕДЕТ ОШИБКУ ВЕРСИИ ptxas!!!
os.environ['PATH'] = '/usr/local/cuda-12.3/bin:' + os.environ['PATH']

LANG_ID = "ru"
MODEL_ID = "bond005/wav2vec2-mbart50-ru"
PATH_MODEL = '/home/redalexdad/recognition_speech/wav2vec2-mbart50-ru'

# Проверка доступности GPU
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = 'cpu'
# Настройка количества процессоров и памяти
num_processes = max(1, os.cpu_count())
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
        wer_score, cer_score, mer_score, wil_score = self.calculate_metrics(reference_text, transcription_text)
        print(
            f"WER: {wer_score:.2f}, "
            f"CER: {cer_score:.2f}, "
            f"MER: {mer_score:.2f}, "
            f"WIL: {wil_score:.2f}"
        )

        # Сохраним транскрипцию в базе данных
        transcription = Transcription(
            text=transcription_text,
            transcription_text=transcription_text,
            wer=wer_score,
            cer=cer_score,
            mer=mer_score,
            wil=wil_score
        )
        transcription.save()
        serializer = TranscriptionSerializer(transcription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
                    num_processes=num_processes,
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

        return wer_score, cer_score, mer_score, wil_score
