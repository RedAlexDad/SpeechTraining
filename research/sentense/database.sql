CREATE TABLE audio_records (
    id SERIAL PRIMARY KEY,
    topic TEXT NOT NULL,
    paragraph_text TEXT NOT NULL,
    transcript_text TEXT NOT NULL,
    voice_recording BYTEA NOT NULL,
    record_date DATE NOT NULL
);
