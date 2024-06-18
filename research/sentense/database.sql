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