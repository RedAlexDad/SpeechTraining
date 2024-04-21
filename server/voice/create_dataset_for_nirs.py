import base64
import os
import time
import psycopg2
import keyboard
import torch
import sounddevice as sd
from datetime import datetime
from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor
from jiwer import wer, cer, mer, wil
from collection import collection  # Предполагается, что у вас есть файл collection.py с коллекцией данных


class SpeechRecognitionSystem:
    def __init__(self):
        self.device = 'cpu'
        self.connect_model()
        self.connect_database()

    def connect_model(self):
        self.NUM_PROCESSES = max(4, os.cpu_count())  # Количество потоков для обучения и предсказния
        self.LANG_ID = 'ru'  # Русский язык
        self.MODEL_ID = 'bond005/wav2vec2-mbart50-ru'  # Название модели
        self.PATH_MODEL = '/home/redalexdad/recognition_speech/wav2vec2-mbart50-ru'  # Путь до модели

        if os.path.exists(self.PATH_MODEL):
            self.processor = Wav2Vec2Processor.from_pretrained(self.PATH_MODEL)
            self.model = SpeechEncoderDecoderModel.from_pretrained(self.PATH_MODEL).to(self.device)
            print('Модель успешно загружена')
        else:
            self.processor = Wav2Vec2Processor.from_pretrained(self.MODEL_ID)
            self.processor.save_pretrained(self.PATH_MODEL)
            self.model = SpeechEncoderDecoderModel.from_pretrained(self.MODEL_ID).to(self.device)
            self.model.save_pretrained(self.PATH_MODEL)
            print(f'Модель успешно загружена и сохранена в {self.PATH_MODEL}')

    def connect_database(self):
        try:
            self.conn = psycopg2.connect(
                dbname="dataset_speech_recognition",
                user="postgres",
                password="postgres",
                host="localhost"
            )
            print("Успешно подключено к базе данных")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recognition_data (
                    id SERIAL PRIMARY KEY,
                    data_recognition BYTEA,
                    transcription_word TEXT,
                    word_for_check TEXT,
                    date_recoding DATE,
                    wer FLOAT,
                    cer FLOAT,
                    mer FLOAT,
                    wil FLOAT,
                    iwer FLOAT
                );
            """)
            self.conn.commit()
            print("Таблица recognition_data успешно создана")
        except Exception as e:
            print(f"Ошибка создания таблицы: {e}")

    def record_audio(self, duration=3, sampling_rate=16000, channels=1):
        try:
            print('Начало записи звука')
            recording = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=channels,
                               dtype='int16')
            sd.wait()
            print('Конец записи звука')
            return recording
        except Exception as e:
            print(f"Ошибка записи звука: {e}")
            return None

    def transcribe_audio(self, audio_data):
        try:
            audio_tensor = torch.FloatTensor(audio_data.squeeze()).to(self.device)
            processed = self.processor(audio_tensor, sampling_rate=16000, return_tensors="pt", padding='longest').to(
                self.device)
            with torch.no_grad():
                predicted_ids = self.model.generate(**processed).to(self.device)
                transcription = self.processor.batch_decode(
                    predicted_ids,
                    num_processes=self.NUM_PROCESSES,
                    skip_special_tokens=True
                )[0]
                return transcription.lower()
        except Exception as e:
            print(f"Ошибка транскрибации аудио: {e}")
            return None

    def insert_recognition_data(self, data_recognition, transcription_word, word_for_check, date_recoding, wer, cer,
                                mer, wil, iwer):
        # Преобразовать массив байтов в строку Base64
        audio_data_base64 = base64.b64encode(data_recognition).decode('utf-8')
        try:
            cursor = self.conn.cursor()
            insert_query = """
                INSERT INTO recognition_data (data_recognition, transcription_word, word_for_check, date_recoding, wer, cer, mer, wil, iwer)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                audio_data_base64, transcription_word, word_for_check, date_recoding, wer, cer, mer, wil, iwer))
            self.conn.commit()
            print("Данные успешно вставлены в базу данных")
        except Exception as e:
            print(f"Ошибка вставки данных: {e}")

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


if __name__ == "__main__":
    recognition_system = SpeechRecognitionSystem()
    for theme, words in collection.items():
        print('=' * 100)
        print(f'Тема: {theme}')
        for word in words:
            print('-' * 100)
            print(f'Слово: {word}')
            print('Приготовьтесь к записи звука...')
            time.sleep(2)
            audio_data = recognition_system.record_audio(duration=2)
            transcription_text = recognition_system.transcribe_audio(audio_data)
            print("Канонический текст:", word)
            print("Распознанный текст:", transcription_text)
            wer_score, cer_score, mer_score, wil_score, iwer_score = (
                recognition_system.calculate_metrics(word, transcription_text))
            recognition_system.insert_recognition_data(
                audio_data, transcription_text, word, datetime.now().date(),
                wer_score, cer_score, mer_score, wil_score, iwer_score
            )
        print('-' * 100)
    print('=' * 100)
