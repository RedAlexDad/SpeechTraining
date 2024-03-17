CREATE TABLE recognition_transcription
(
    id                 SERIAL PRIMARY KEY,
    text               TEXT,
    transcription_text TEXT,
    WER                TEXT,
    CER                TEXT,
    MER                TEXT,
    WIL                TEXT
);
