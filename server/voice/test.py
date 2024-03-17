import os
import warnings

import torch
import torchaudio
import sounddevice as sd

from datasets import load_dataset, load_from_disk
from datasets.features import Audio
from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor
import pandas as pd
import numpy as np

LANG_ID = "ru"
MODEL_ID = "bond005/wav2vec2-mbart50-ru"
PATH_MODEL = '/home/redalexdad/recognition_speech/wav2vec2-mbart50-ru'
# Кол-во текстов для предсказания
SAMPLES = 1
device = 'cpu'

torch.cuda.empty_cache()
num_processes = max(1, os.cpu_count())

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


# Функция записи голоса и возврата в виде массива для предсказания
def record_audio(duration=3, sampling_rate=16000):
    print('Начало записи звука')
    recording = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=1, dtype='int16')
    sd.wait()
    print('Конец записи звука')
    return recording


# Функция распознавания голоса, т.е. транскрибация
def transcribe_audio(audio_data, model, processor, device):
    # Преобразование данных аудио в тензор
    # audio_tensor = torch.from_numpy(audio_data).unsqueeze(0)
    # Предварительная обработка записанного аудио
    audio_tensor = torch.FloatTensor(audio_data.squeeze()).to(device)

    # Предобработка данных
    processed = processor(audio_tensor, sampling_rate=16000, return_tensors="pt", padding='longest').to(device)
    try:
        with torch.no_grad():
            predicted_ids = model.generate(**processed).to(device)

            # Декодирование предсказаний
            predicted_sentences = processor.batch_decode(
                predicted_ids,
                num_processes=num_processes,
                skip_special_tokens=True
            )[0]

            # predicted_sentences = processor.batch_decode(predicted_ids, skip_special_tokens=True)
            return predicted_sentences
    except Exception as error:
        print('ERROR: ', error)
        return error

# Функция проверки метрики WER (Word Error Rate)
def calculate_wer(reference_text, transcription_text):
    # Здесь должна быть реализация подсчета WER
    wer = 0  # Замените это на ваш код расчета WER
    return wer


# Пример использования функций
# Запись голоса
audio_data = record_audio()
# Распознавание голоса
transcription_text = transcribe_audio(audio_data, model, processor, device)
# Проверка метрики WER
reference_text = 'Привет'
wer = calculate_wer(reference_text, transcription_text)

print("Канонический текст:", reference_text)
print("Распознанный текст:", transcription_text)
