import base64
import os
import time
import uuid
import numpy as np
import psycopg2
import torch
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor
from jiwer import wer, cer, mer, wil
from research.word.collection import collection


# from google.cloud import speech_v1p1beta1 as speech

class SpeechRecognitionSystem:
    def __init__(self, collection, run_model=True):
        # Использование CPU для предсказания модели
        self.device = 'cpu'
        # Подключение к БД
        self.connect_database()
        # Коллекция данных для тренировки произношения и установки метрики
        self.collection = collection
        # Путь для сохранения звука
        self.save_path = '/home/redalexdad/GitHub/SpeechTraining/server/voice/dataset/'
        # Инициализация клиента Google Cloud Speech-to-Text
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "путь_к_моему_json_ключу" # Нужно разобраться с этим, попозже
        # self.client = speech.SpeechClient()
        # Запуск модели (несколько времени занимает)
        self.connect_model() if run_model else setattr(self, 'connect_model', None)

    def set_save_path(self, path) -> None:
        self.save_path = path

    def connect_model(self) -> None:
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

    def connect_database(self) -> None:
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

    def create_table(self) -> None:
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

    def record_audio(self, duration=3, sampling_rate=16000, channels=1) -> np.ndarray or None:
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

    def transcribe_audio(self, audio_data) -> str or None:
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
                                mer, wil, iwer) -> None:
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
    def calculate_metrics(self, reference_text, transcription_text) -> tuple[float, float, float, float, float]:
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

    def iwer(self, reference_sentence, hypothesis_sentence) -> float:
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

    def listen_to_audio_by_index(self, index) -> bytes or None:
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT data_recognition
                FROM recognition_data
                WHERE id = %s;
            """, (index,))
            audio_data_base64 = cursor.fetchone()[0]
            audio_data = base64.b64decode(audio_data_base64)
            return audio_data
        except Exception as e:
            print(f"Ошибка получения аудио записи: {e}")
            return None

    def play_audio(self, audio_data, sampling_rate=16000) -> None:
        try:
            # Преобразование байтовых данных аудио в формат int16
            audio_array = np.frombuffer(audio_data, dtype='int16')
            print('Воспроизведение аудио...')
            sd.play(audio_array, samplerate=sampling_rate)
            sd.wait()
            print('Воспроизведение завершено.')
        except Exception as e:
            print(f"Ошибка воспроизведения аудио: {e}")

    def save_audio(self, audio_data, sampling_rate=16000) -> None:
        try:
            audio_array = np.frombuffer(audio_data, dtype='int16')
            filename = f'audio_{str(uuid.uuid4())[:8]}.wav'
            full_filename = f'{self.save_path}/{filename}'
            sf.write(full_filename, audio_array, samplerate=sampling_rate)
            print(f'Аудио сохранено как {filename}')
        except Exception as e:
            print(f'Ошибка сохранения аудио: {e}')

    # def recognize_speech_google(self, audio_data, language_code="ru-RU"):
    #     try:
    #         # Определение конфигурации аудио
    #         audio = speech.RecognitionAudio(content=audio_data)
    #         config = speech.RecognitionConfig(
    #             encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #             sample_rate_hertz=16000,
    #             language_code=language_code,
    #         )
    #         # Выполнение запроса к Google Cloud Speech-to-Text API
    #         response = self.client.recognize(config=config, audio=audio)
    #         # Извлечение текста из распознанной речи
    #         text = ""
    #         for result in response.results:
    #             text += result.alternatives[0].transcript
    #         return text
    #     except Exception as e:
    #         print(f"Ошибка распознавания речи через Google: {e}")
    #         return None

    def run(self) -> None:
        if self.connect_model is None:
            raise ConnectionError("Модель не подключена!. Не забудьте включить, например, run_model=True в SpeechRecognitionSystem(collection, run_model=True)")

        for theme_num, (theme, words) in enumerate(collection.items(), start=1):
            print('=' * 100)
            print(f'Тема {theme_num} / {len(collection)}: {theme}')
            for word_num, word in enumerate(words, start=1):
                print('-' * 100)
                print(f'Слово {word_num} / {len(words)}: {word}')
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


if __name__ == "__main__":
    recognition_system = SpeechRecognitionSystem(collection, run_model=True)

    # Прослушка запись звука
    # audio_data = recognition_system.listen_to_audio_by_index(20)
    # recognition_system.play_audio(audio_data)
    # recognition_system.save_audio(audio_data)

    # Запуск модели для распознавания речи
    recognition_system.run()