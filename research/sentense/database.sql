CREATE TABLE audio_records (
    id SERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    paragraph_text TEXT NOT NULL,
    transcript_text_yandex TEXT NOT NULL,
    transcript_text_salutespeech TEXT NOT NULL,
    transcript_text_mbart50 TEXT NOT NULL,
    voice_recording BYTEA NOT NULL,
    record_date TIMESTAMP NOT NULL
);

SELECT 
    DATE(record_date) AS date,  -- Извлекаем только дату из столбца record_date
    COUNT(*) AS record_count    -- Считаем количество записей за каждый день
FROM 
    audio_records
GROUP BY 
    DATE(record_date)           -- Группируем по дате
ORDER BY 
    DATE(record_date);          -- Упорядочиваем результат по дате
