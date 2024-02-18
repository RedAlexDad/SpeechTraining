from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transcription
from .serializers import TranscriptionSerializer
from django.http import Http404

from transformers import AutoTokenizer, Wav2Vec2ForCTC
import torch
import torchaudio
import jiwer
import sounddevice as sd
import time

from Web.settings import BASE_DIR

# Загрузка модели и токенизатора
tokenizer = AutoTokenizer.from_pretrained(
    "Edresson/wav2vec2-large-100k-voxpopuli-ft-Common-Voice_plus_TTS-Dataset-russian")
model = Wav2Vec2ForCTC.from_pretrained(
    "Edresson/wav2vec2-large-100k-voxpopuli-ft-Common-Voice_plus_TTS-Dataset-russian")


class TranscriptionView(APIView):
    def post(self, request, format=None):
        # Получим предложения из запроса
        sentences = request.data.get('sentences', None)
        reference_text = " ".join(sentence.lower() for sentence in sentences)

        # Выполним запись и транскрибацию
        transcription_text = self.record_and_transcribe()
        print("Канонический текст:", reference_text)
        print("Распознанный текст:", transcription_text)

        # Проверяем на точность произношения
        error_percentage = self.calculate_error_percentage(reference_text, transcription_text)
        print("Процент ошибок: {:.2f}%".format(error_percentage))

        # Сохраним транскрипцию в базе данных
        transcription = Transcription(text=transcription_text, transcription_text=transcription_text, error_percentage=error_percentage)
        transcription.save()
        serializer = TranscriptionSerializer(transcription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def record_and_transcribe(self):
        # Запись звука
        print('Начало записи звука')
        # Запись голоса и сохранение в формате WAV
        recording = sd.rec(int(3 * 44100), samplerate=44100, channels=1, dtype='int16')
        sd.wait()
        # Преобразуем 1D тензор в 2D, добавив размерность пакета
        recording = torch.from_numpy(recording.squeeze()).unsqueeze(0)
        torchaudio.save(f"{BASE_DIR}/voice/recorded_audio.wav", recording, 44100)
        print('Конец записи звука')

        # Загрузка записанного аудиофайла
        audio_path = f"{BASE_DIR}/voice/recorded_audio.wav"
        speech, _ = torchaudio.load(audio_path)

        # Преобразование с использованием модели
        resampler = torchaudio.transforms.Resample(orig_freq=48_000, new_freq=16_000)
        input_values = resampler.forward(speech.squeeze(0)).numpy()

        # Токенизация и получение предсказания от модели
        input_values = torch.tensor(input_values).unsqueeze(0)  # добавляем размерность пакета
        with torch.no_grad():
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)

        # Декодирование предсказанных токенов в текст
        transcription = tokenizer.batch_decode(predicted_ids)[0]

        return transcription

    def calculate_error_percentage(self, reference_text, transcription_text):
        total_chars = max(len(reference_text), len(transcription_text))
        incorrect_chars = sum(
            [1 for char_ref, char_trans in zip(reference_text, transcription_text) if char_ref != char_trans])
        error_percentage = round((incorrect_chars / total_chars) * 100, 3)
        return error_percentage
