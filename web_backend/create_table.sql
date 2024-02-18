CREATE TABLE recognition_transcription
(
    id                 SERIAL PRIMARY KEY,
    text               TEXT,
    transcription_text TEXT,
    error_percentage   TEXT
);
