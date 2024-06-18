import psycopg2
from psycopg2 import sql
from datetime import datetime

class AudioRecorderDB:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def create_table(self):
        create_table_query = """
            CREATE TABLE audio_records (
                id SERIAL PRIMARY KEY,
                topic TEXT NOT NULL,
                paragraph_text TEXT NOT NULL,
                transcript_text_yandex TEXT NOT NULL,
                transcript_text_salutespeech TEXT NOT NULL,
                transcript_text_mbart TEXT NOT NULL,
                voice_recording BYTEA NOT NULL,
                record_date TIMESTAMP NOT NULL
            );
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def insert_record(self, topic, paragraph_text, transcript_text_yandex, transcript_text_salutespeech,
                      transcript_text_mbart50, voice_recording):
        insert_query = sql.SQL(
            "INSERT INTO audio_records (topic, paragraph_text, transcript_text_yandex, transcript_text_salutespeech, transcript_text_mbart50, voice_recording, record_date) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        record_date = datetime.now()
        self.cur.execute(insert_query, (
            topic, paragraph_text, transcript_text_yandex, transcript_text_salutespeech, transcript_text_mbart50,
            psycopg2.Binary(voice_recording),
            record_date
        ))
        self.conn.commit()

# Пример использования класса
# recorder_db = AudioRecorderDB(dbname='your_database_name', user='your_username', password='your_password', host='your_host', port='your_port')
# recorder_db.connect()
# recorder_db.create_table()
# recorder_db.insert_record(topic='Тема текста', paragraph_text='Текст абзаца', voice_recording=b'binary_data_here')
# recorder_db.disconnect()
