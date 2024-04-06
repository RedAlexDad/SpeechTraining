import os

from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RecognitionData, Metric
from .serializers import RecognitionDataSerializer

import torch
import sounddevice as sd

# Для теста WER - Word Error Rate, CER - Character Error Rate, MER - Match Error Rate, WIL - Word Information Lost
from jiwer import wer, cer, mer, wil

class TranscriptionView(APIView):
    def __init__(self, MODEL_ID: str = "bond005/wav2vec2-mbart50-ru", device: str = 'cpu', **kwargs):
        super().__init__(**kwargs)
        # НЕ УБИРАЙТЕ ЭТУ ЯЧЕЙКУ, ИНАЧНЕ БУДЕТ НЕПРАВИЛЬНО ИНИЦИАЛИЗИРОВАНО ОКРУЖЕНИЕ, ЧТО И ВЫВЕДЕТ ОШИБКУ ВЕРСИИ ptxas!!!
        os.environ['PATH'] = '/usr/local/cuda-12.3/bin:' + os.environ['PATH']

        self.LANG_ID = "ru"
        self.MODEL_ID = MODEL_ID
        self.PATH_MODEL = '/home/redalexdad/recognition_speech/wav2vec2-mbart50-ru'
        self.device = device

        # Проверка доступности GPU
        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # Настройка количества процессоров и памяти
        self.NUM_PROCESSES = max(1, os.cpu_count())
        # print(f"Using device: {device}")

        # Устанавливает максимальное количество доступной видеопамяти (например, 75%)
        # torch.cuda.set_per_process_memory_fraction(0.75)
        # Включает динамическое выделение памяти на GPU
        # torch.cuda.set_per_process_memory_growth(True)

        # Проверка наличия модели в локальном пути
        if os.path.exists(self.PATH_MODEL):
            # Загрузка процессора из локального пути
            self.processor = Wav2Vec2Processor.from_pretrained(self.PATH_MODEL)

            # Загрузка модели из локального пути
            self.model = SpeechEncoderDecoderModel.from_pretrained(self.PATH_MODEL).to(device)
            print('Успешно модель загружена')
        else:
            # Загрузка процессора из сети и сохранение в локальный путь
            self.processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
            self.processor.save_pretrained(self.PATH_MODEL)

            # Загрузка модели из сети и сохранение в локальный путь
            self.model = SpeechEncoderDecoderModel.from_pretrained(MODEL_ID).to(device)
            self.model.save_pretrained(self.PATH_MODEL)
            print(f'Успешно модель скачана и сохранена в пути {self.PATH_MODEL}')

    def post(self, request, format=None):
        # Получим предложения из запроса
        sentences = request.data.get('sentences', None)
        reference_text = " ".join(sentence.lower() for sentence in sentences)

        # Запись голоса
        audio_data = self.record_audio()
        # Распознавание голоса
        transcription_text = self.transcribe_audio(audio_data, self.model, self.processor, self.device)

        print("Канонический текст:", reference_text)
        print("Распознанный текст:", transcription_text)

        # Проверяем на точность произношения
        wer_score, cer_score, mer_score, wil_score, iwer_score = self.calculate_metrics(reference_text,
                                                                                        transcription_text)
        print(
            f"WER: {wer_score:.2f}, "
            f"CER: {cer_score:.2f}, "
            f"MER: {mer_score:.2f}, "
            f"WIL: {wil_score:.2f}"
            f"IWER: {iwer_score:.2f}"
        )

        # Создаем объект метрики
        metric = Metric.objects.create(
            WER=wer_score,
            CER=cer_score,
            MER=mer_score,
            WIL=wil_score,
            IWER=iwer_score
        )

        # Сохраним транскрипцию в базе данных
        transcription = RecognitionData(
            text=transcription_text,
            transcription_text=transcription_text,
            id_metric=metric.id,
        )
        transcription.save()
        serializer = RecognitionDataSerializer(transcription)
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
                    num_processes=self.NUM_PROCESSES,
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
        iwer_score = self.iwer(reference_text, transcription_text)

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

        # Считаем количество совпадающих слов
        matching_words = sum(1 for ref, hyp in zip(reference_words, hypothesis_words) if ref == hyp)

        # Вычисляем Inflectional Word Error Rate (IWER)
        iwer_score = (total_words - matching_words) / total_words * 100

        return iwer_score
