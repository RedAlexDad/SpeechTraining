# Для взаимодействия с системой
import os
import re
import sys
# Для работы с массивами чисел
import numpy as np 
# Для работы с данными в формате DataFrame
import pandas as pd
# Для работы со звуковыми файлами
import io
import soundfile as sf
import librosa
# Для работы с различными сервисами распознавания речи
from AutomaticSpeechRecognitionYandex import AutomaticSpeechRecognitionYandex
from AutomaticSpeechRecognitionSaluteSpeech import AutomaticSpeechRecognitionSaluteSpeech
from AutomaticSpeechRecognitionMBART50 import AutomaticSpeechRecognitionMBART50

from tokens import FOLDER_ID, OAUTH, CLIENT_ID, CLIENT_SECRET


class TranscriptUpdater:
    def __init__(self, df, yandex_asr: AutomaticSpeechRecognitionYandex, salute_asr: AutomaticSpeechRecognitionSaluteSpeech, mbart_asr: AutomaticSpeechRecognitionMBART50):
        self.df = df
        self.yandex_asr = yandex_asr
        self.salute_asr = salute_asr
        self.mbart_asr = mbart_asr

    def is_invalid_transcript(self, transcript: str):
        """Проверяет, содержит ли текст ошибки или является пустым."""
        return pd.isna(transcript) or transcript.strip() == "" or "Ошибка" in transcript.lower() or "http error" in transcript.lower()

    def update_transcripts(self):
        """Перезаписывает транскрипции для строк с ошибками или пустыми значениями."""
        for index, row in self.df.iterrows():

            # Проверяем колонку Yandex
            if self.is_invalid_transcript(str(row['transcript_text_yandex'])):
                print(f"Перезапись Yandex для ID: {index}")
                # print(type(row['voice_recording']))
                audio_data = self.load_audio_from_path(row['voice_recording']) # Получаем данные аудио из строки
                if audio_data is not None:
                    old_transcript_yandex = row['transcript_text_yandex']
                    try:
                        audio_data = self.trim_audio(audio_data) # Обрезаем до 30 секунд
                        new_transcript_yandex = self.yandex_asr.recognize_speech_audio_data(audio_data, print_result=False)

                        # Check if new_transcript_yandex is a single string or a list/array
                        if isinstance(new_transcript_yandex, str):
                            new_transcript_yandex = [new_transcript_yandex]
                        
                        if self.is_invalid_transcript(new_transcript_yandex):
                            self.df.at[index, 'transcript_text_yandex'] = None
                            print(f"Не удалось распознать текст Yandex для ID: {index}. Установлено значение None.")
                        else:
                            self.df.at[index, 'transcript_text_yandex'] = new_transcript_yandex
                            print(f"Исправлено Yandex для ID: {index}. Старый текст: {old_transcript_yandex}, Новый текст: {new_transcript_yandex}")
                    except Exception as e:
                        print(f"Ошибка при распознавании Yandex для ID: {index}: {e}")
                        # Присваиваем None в случае ошибки
                        self.df.at[index, 'transcript_text_yandex'] = None
                else:
                    print(f"Ошибка: отсутствует аудиофайл для Yandex ID: {index}")

            # Проверяем колонку SaluteSpeech
            if self.is_invalid_transcript(str(row['transcript_text_salutespeech'])):
                print(f"Перезапись SaluteSpeech для ID: {index}")
                audio_data = self.load_audio_from_path(row['voice_recording']) # Получаем данные аудио из строки
                if audio_data is not None:
                    old_transcript_salutespeech = row['transcript_text_salutespeech']
                    try:
                        # audio_data = self.trim_audio(audio_data) # Обрезаем до 30 секунд
                        new_transcript_salutespeech = self.salute_asr.recognize_speech_salute(audio_data, print_result=False)
                        if self.is_invalid_transcript(new_transcript_yandex):
                            self.df.at[index, 'transcript_text_salutespeech'] = None
                            print(f"Не удалось распознать текст SaluteSpeech для ID: {index}. Установлено значение None.")
                        else:
                            self.df.at[index, 'transcript_text_salutespeech'] = new_transcript_salutespeech
                            print(f"Исправлено SaluteSpeech для ID: {index}. Старый текст: {old_transcript_salutespeech}, Новый текст: {new_transcript_salutespeech}")
                    except Exception as e:
                        print(f"Ошибка при распознавании SaluteSpeech для ID: {index}: {e}")
                        # Присваиваем None в случае ошибки
                        self.df.at[index, 'transcript_text_salutespeech'] = None
                else:
                    print(f"Ошибка: отсутствует аудиофайл для SaluteSpeech ID: {index}")

            # Проверяем колонку MBART50
            if self.is_invalid_transcript(str(row['transcript_text_mbart50'])):
                print(f"Перезапись MBART50 для ID: {index}")
                audio_data = self.load_audio_from_path(row['voice_recording']) # Получаем данные аудио из строки
                if audio_data is not None:
                    old_transcript_mbart50 = row['transcript_text_mbart50']
                    try:
                        audio_data = self.trim_audio(audio_data) # Обрезаем до 30 секунд
                        new_transcript_mbart50 = self.mbart_asr.transcribe_audio(audio_data, print_result=False)
                        if self.is_invalid_transcript(new_transcript_yandex):
                            self.df.at[index, 'transcript_text_mbart50'] = None
                            print(f"Не удалось распознать текст MBART50 для ID: {index}. Установлено значение None.")
                        else:
                            self.df.at[index, 'transcript_text_mbart50'] = new_transcript_mbart50
                            print(f"Исправлено MBART50 для ID: {index}. Старый текст: {old_transcript_mbart50}, Новый текст: {new_transcript_mbart50}")
                    except Exception as e:
                        print(f"Ошибка при распознавании SaluteSpeech для ID: {index}: {e}")
                        # Присваиваем None в случае ошибки
                        self.df.at[index, 'transcript_text_mbart50'] = None
                else:
                    print(f"Ошибка: отсутствует аудиофайл для MBART50 ID: {index}")


    def load_audio_from_path(self, audio_data):
        """Загружает аудиоданные из строки."""
        try:
            # Convert string to bytes
            audio_bytes = self.string_to_bytes(audio_data)
            
            # Ensure the audio data is in int16 format
            audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
            
            # Resample to 16000 Hz if necessary
            sample_rate = 16000
            if audio_array.shape[0] // sample_rate > 30:
                print("Аудио длиннее 30 секунд, обрезаем до 30 секунд.")
                audio_array = audio_array[:30 * sample_rate]
            
            # Ensure the audio data is in the correct format (int16, little-endian)
            if audio_array.dtype != np.int16 or audio_array.itemsize != 2:
                print("Преобразуем аудио в int16 формат.")
                audio_array = audio_array.astype(np.int16).tobytes().decode('latin-1').encode('utf-8')
            
            return audio_array
        except Exception as e:
            print(f"Ошибка загрузки аудио файла: {e}")
        return None



    def trim_audio(self, audio_data, max_seconds=30):
        """Обрезает аудио до заданной длины."""
        sample_rate = 16000
        max_samples = int(max_seconds * sample_rate)
        if len(audio_data) > max_samples:
            print(f"Аудио длиннее {max_seconds} секунд ({len(audio_data)} сэмплов), обрезаем до {max_samples} сэмплов.")
            audio_data = audio_data[:max_samples]  # Обрезаем NumPy массив
        else:
            print(f"Аудио короче {max_seconds} секунд ({len(audio_data)} сэмплов), обрезка не требуется.")

        # Преобразуем NumPy массив обратно в байты
        with io.BytesIO() as f:
            sf.write(f, audio_data, sample_rate, format='WAV')
            return f.getvalue()
        
    @staticmethod
    def string_to_bytes(audio_string):
        return audio_string.encode('utf-8')
    
    @staticmethod
    def is_yandex_compatible_audio(audio_data):
        max_size_mb = 1  # Maximum allowed size in MB
        max_duration_seconds = 30  # Maximum allowed duration in seconds
        
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        sample_rate = 16000
        
        # Check size
        audio_bytes = len(audio_data)
        if audio_bytes / 1024 / 1024 > max_size_mb:
            return False, f"Audio too large ({audio_bytes / 1024 / 1024:.2f} MB). Maximum allowed size: {max_size_mb} MB."
        
        # Check duration
        audio_duration = len(audio_array) / sample_rate
        if audio_duration > max_duration_seconds:
            return False, f"Audio too long ({audio_duration:.2f} seconds). Maximum allowed duration: {max_duration_seconds} seconds."
        
        return True, ""

        
        
if __name__ == "__main__":
    df = pd.read_csv('/home/redalexdad/GitHub/SpeechTraining/research/sentense/database.csv')
    df.info()

    # Преобразование столбца record_date в формат datetime
    df['record_date'] = pd.to_datetime(df['record_date'])
    # Сбросим datetime чтобы сделать группировку, иначе не получим из за уникальности
    df['record_date'] = df['record_date'].dt.date
    # df['voice_recording'] = bytearray(audio_data)  # Преобразуем в байтовый массив

    # Группируем только числовые столбцы
    df_grouped = df.groupby(['record_date', 'id']).sum()

    # Копируем столбец voice_recording из исходного DataFrame в сгруппированный
    df_grouped['voice_recording'] = df['voice_recording']

    df.info()
    df.head()
    
    yandex_asr = AutomaticSpeechRecognitionYandex(FOLDER_ID, OAUTH)
    salute_asr = AutomaticSpeechRecognitionSaluteSpeech(CLIENT_ID, CLIENT_SECRET)
    
    # # Обновление транскрипций в датасете
    transcript_updater = TranscriptUpdater(df, yandex_asr, salute_asr, mbart_asr=None)
    transcript_updater.update_transcripts()