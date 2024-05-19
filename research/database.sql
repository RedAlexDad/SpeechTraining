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

-- SQL-запрос, который выводит общее количество слов, записанных в каждый день. Для этого можно использовать следующий запрос:
SELECT
    date_recoding,
    COUNT(*) AS word_count
FROM
    recognition_data
GROUP BY
    date_recoding
ORDER BY
    date_recoding;

-- Запрос, который выводит общее количество:
SELECT COUNT(*) FROM recognition_data;
