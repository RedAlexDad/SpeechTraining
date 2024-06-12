import psycopg2
import pandas as pd

# Соединение с БД
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="dataset_speech_recognition",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()

# Получение данных из таблицы
cur.execute("SELECT * FROM recognition_data")
data = cur.fetchall()

# Закрытие соединения
cur.close()
conn.close()

# Создание DataFrame из полученных данных
df = pd.DataFrame(data, columns=['id', 'data_recognition', 'transcription_word', 'word_for_check', 'date_recoding', 'wer', 'cer', 'mer', 'wil', 'iwer'])

# Экспорт DataFrame в CSV файл
df.to_csv('database.csv', index=False)
