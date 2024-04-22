CREATE DATABASE dataset_speech_recognition;

CREATE TABLE IF NOT EXISTS recognition_data
(
    id                 SERIAL PRIMARY KEY,
    data_recognition   BYTEA,
    transcription_word TEXT,
    word_for_check     TEXT,
    date_recoding      DATE,
    wer                FLOAT,
    cer                FLOAT,
    mer                FLOAT,
    wil                FLOAT,
    iwer               FLOAT
);


SELECT *
FROM recognition_data;