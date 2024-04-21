import os
import time
from datetime import datetime
# Установим соединение с базой данных PostgreSQL
import psycopg2
# Для машинного обучения
from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor
import torch
import sounddevice as sd

# Для теста WER - Word Error Rate, CER - Character Error Rate, MER - Match Error Rate, WIL - Word Information Lost
from jiwer import wer, cer, mer, wil
# Получаем коллекцию данных
from collection import collection

def connect_model():
    # Проверка доступности GPU
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Настройка количества процессоров и памяти
    NUM_PROCESSES = max(1, os.cpu_count())
    # print(f"Using device: {device}")

    # Устанавливает максимальное количество доступной видеопамяти (например, 75%)
    # torch.cuda.set_per_process_memory_fraction(0.75)
    # Включает динамическое выделение памяти на GPU
    # torch.cuda.set_per_process_memory_growth(True)

    # НЕ УБИРАЙТЕ ЭТУ ЯЧЕЙКУ, ИНАЧНЕ БУДЕТ НЕПРАВИЛЬНО ИНИЦИАЛИЗИРОВАНО ОКРУЖЕНИЕ, ЧТО И ВЫВЕДЕТ ОШИБКУ ВЕРСИИ ptxas!!!
    os.environ['PATH'] = '/usr/local/cuda-12.3/bin:' + os.environ['PATH']

    LANG_ID = 'ru'
    MODEL_ID = 'bond005/wav2vec2-mbart50-ru'
    PATH_MODEL = '/home/redalexdad/recognition_speech/wav2vec2-mbart50-ru'
    device = 'cpu'

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

def connect_database():
    conn = psycopg2.connect(
        dbname="dataset_speech_recognition",
        user="posgres",
        password="posgres",
        host="localhost"
    )

def create_database(conn):
    # Создание таблицы RecognitionData
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE recognition_data (
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

    conn.commit()
    # Закрываем соединение
    conn.close()

def insert_recognition_data(conn, data_recognition, transcription_word, word_for_check, date_recoding, wer, cer, mer, wil, iwer):
    # Создаем курсор для выполнения SQL-запросов
    cursor = conn.cursor()
    # SQL-запрос для вставки данных
    insert_query = """
        INSERT INTO recognition_data (data_recognition, transcription_word, word_for_check, date_recoding, wer, cer, mer, wil, iwer)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    # Выполняем SQL-запрос с данными
    cursor.execute(insert_query,(data_recognition, transcription_word, word_for_check, date_recoding, wer, cer, mer, wil, iwer))
    # Подтверждаем изменения в базе данных
    conn.commit()
    # Закрываем соединение с базой данных
    conn.close()

for theme, words in collection.items():
    for word in words:
        # Запись голоса
        print('Приготовьтесь к записи голоса...')
        time.sleep(1)
        audio_data = record_audio(duration=1, sampling_rate=16000, channels=1)
        transcription_text = transcribe_audio(audio_data, model, processor, device)

        print("Канонический текст:", word)
        print("Распознанный текст:", transcription_text)

        # Проверяем на точность произношения
        wer_score, cer_score, mer_score, wil_score, iwer_score = calculate_metrics(word, transcription_text)
