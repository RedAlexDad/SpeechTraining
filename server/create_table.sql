CREATE TABLE account
(
    id            SERIAL PRIMARY KEY,
    name          TEXT    NOT NULL,
    lastname      TEXT    NOT NULL,
    fathername    TEXT    NOT NULL,
    username      TEXT    NOT NULL,
    password      TEXT    NOT NULL,
    is_logopedist BOOLEAN NOT NULL
);

CREATE TABLE data_recognition_and_synthesis
(
    id             SERIAL PRIMARY KEY,
    id_synthesis   INTEGER,
    id_recognition INTEGER,
    id_client      INTEGER
);

CREATE TABLE recognition_data
(
    id                 SERIAL PRIMARY KEY,
    data_recognition   BYTEA,
    text_for_check     TEXT,
    transcription_text TEXT,
    date_recoding      DATE,
    wer                FLOAT,
    cer                FLOAT,
    mer                FLOAT,
    wil                FLOAT,
    iwer               FLOAT
);

CREATE TABLE synthesis_data
(
    id               SERIAL PRIMARY KEY,
    data_recognition BYTEA,
    text_synthesis   TEXT,
    text_input       TEXT,
    date_synthesis   DATE,
    wer              FLOAT,
    f1_score         FLOAT
);

CREATE TABLE recommendation
(
    id                                SERIAL PRIMARY KEY,
    id_logodedist                     INTEGER,
    id_data_recognition_and_synthesis INTEGER,
    recommendation_type               TEXT,
    recommendation_text_by_llm        TEXT,
    recommendation_text_by_logopedist TEXT,
    date_recommendation               DATE
);

-- СВЯЗЫВАНИЕ БД ВНЕШНИМИ КЛЮЧАМИ --
ALTER TABLE data_recognition_and_synthesis
    ADD CONSTRAINT FR_data_recognition_and_synthesis_of_account
        FOREIGN KEY (id_client) REFERENCES account (id);

ALTER TABLE data_recognition_and_synthesis
    ADD CONSTRAINT FR_data_recognition_and_synthesis_of_synthesis_data
        FOREIGN KEY (id_synthesis) REFERENCES synthesis_data (id);

ALTER TABLE data_recognition_and_synthesis
    ADD CONSTRAINT FR_data_recognition_and_synthesis_of_recognition_data
        FOREIGN KEY (id_recognition) REFERENCES recognition_data (id);

ALTER TABLE recommendation
    ADD CONSTRAINT FR_recommendation_of_recognition_data
        FOREIGN KEY (id_logodedist) REFERENCES account (id);

ALTER TABLE recommendation
    ADD CONSTRAINT FR_recommendation_of_data_recognition_and_synthesis
        FOREIGN KEY (id_data_recognition_and_synthesis) REFERENCES data_recognition_and_synthesis (id);



-- Данные для таблицы "account"
INSERT INTO account (name, lastname, fathername, username, password, is_logopedist)
VALUES ('Иван', 'Иванов', 'Иванович', 'ivan', 'ivan123', true),
       ('Петр', 'Петров', 'Петрович', 'petr', 'petr123', false),
       ('Анна', 'Сидорова', 'Петровна', 'anna', 'anna123', false),
       ('Елена', 'Козлова', 'Андреевна', 'elena', 'elena123', true),
       ('Сергей', 'Николаев', 'Владимирович', 'sergey', 'sergey123', false);
SELECT *
FROM account;

-- Добавление данных в таблицу recognition_data
INSERT INTO recognition_data (data_recognition, text_for_check, transcription_text, date_recoding, wer, cer, mer, wil,
                              iwer)
VALUES ('binary_data_1', 'Текст для проверки 1', 'Текст транскрибации 1', '2023-01-01', 0.1, 0.2, 0.3, 0.4, 0.5),
       ('binary_data_2', 'Текст для проверки 2', 'Текст транскрибации 2', '2023-02-01', 0.2, 0.3, 0.4, 0.5, 0.6),
       ('binary_data_3', 'Текст для проверки 3', 'Текст транскрибации 3', '2023-03-01', 0.3, 0.4, 0.5, 0.6, 0.7),
       ('binary_data_4', 'Текст для проверки 4', 'Текст транскрибации 4', '2023-04-01', 0.4, 0.5, 0.6, 0.7, 0.8),
       ('binary_data_5', 'Текст для проверки 5', 'Текст транскрибации 5', '2023-05-01', 0.5, 0.6, 0.7, 0.8, 0.9);

SELECT *
FROM recognition_data;

-- Добавление данных в таблицу synthesis_data
INSERT INTO synthesis_data (data_recognition, text_synthesis, text_input, date_synthesis, wer, f1_score)
VALUES ('binary_data_synthesis_1', 'Текст синтеза 1', 'Введенный текст 1', '2023-01-01', 0.1, 0.9),
       ('binary_data_synthesis_2', 'Текст синтеза 2', 'Введенный текст 2', '2023-02-01', 0.2, 0.8),
       ('binary_data_synthesis_3', 'Текст синтеза 3', 'Введенный текст 3', '2023-03-01', 0.3, 0.7),
       ('binary_data_synthesis_4', 'Текст синтеза 4', 'Введенный текст 4', '2023-04-01', 0.4, 0.6),
       ('binary_data_synthesis_5', 'Текст синтеза 5', 'Введенный текст 5', '2023-05-01', 0.5, 0.5);

SELECT *
FROM synthesis_data;

-- Добавление данных в таблицу data_recognition_and_synthesis
INSERT INTO data_recognition_and_synthesis (id_synthesis, id_recognition, id_client)
VALUES (1, 1, 2),
       (2, 2, 3),
       (3, 3, 4),
       (4, 4, 5),
       (5, 5, 1);

SELECT *
FROM data_recognition_and_synthesis;

-- Добавление данных в таблицу recommendation
INSERT INTO recommendation (id_logodedist, id_data_recognition_and_synthesis, recommendation_type,
                            recommendation_text_by_llm, recommendation_text_by_logopedist, date_recommendation)
VALUES (1, 1, 'Тип рекомендации 1', 'Текст рекомендации (LLM) 1', 'Текст рекомендации (логопед) 1', '2023-01-01'),
       (2, 2, 'Тип рекомендации 2', 'Текст рекомендации (LLM) 2', 'Текст рекомендации (логопед) 2', '2023-02-01'),
       (3, 3, 'Тип рекомендации 3', 'Текст рекомендации (LLM) 3', 'Текст рекомендации (логопед) 3', '2023-03-01'),
       (4, 4, 'Тип рекомендации 4', 'Текст рекомендации (LLM) 4', 'Текст рекомендации (логопед) 4', '2023-04-01'),
       (5, 5, 'Тип рекомендации 5', 'Текст рекомендации (LLM) 5', 'Текст рекомендации (логопед) 5', '2023-05-01');


SELECT *
FROM recommendation;