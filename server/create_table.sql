-- CREATE DATABASE trainer;

CREATE TABLE account
(
    id            SERIAL PRIMARY KEY,
    name          TEXT    NOT NULL,
    lastname      TEXT    NOT NULL,
    fathername    TEXT    NOT NULL,
    username      TEXT    NOT NULL,
    password      TEXT    NOT NULL,
    is_moderator BOOLEAN NOT NULL
);

CREATE TABLE recognition_data
(
    id                 SERIAL PRIMARY KEY,
    data_recognition   BYTEA,
    word_for_check     TEXT,
    transcription_word TEXT,
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
    word_synthesis   TEXT,
    word_input       TEXT,
    date_synthesis   DATE,
    wer              FLOAT
);

CREATE TABLE recommendation
(
    id                                SERIAL PRIMARY KEY,
    logodedist_id                     INTEGER,
    data_recognition_and_synthesis_id INTEGER,
    recommendation_type               TEXT,
    recommendation_text_by_llm        TEXT,
    recommendation_text_by_logopedist TEXT,
    date_recommendation               DATE
);

CREATE TABLE text (
    id SERIAL PRIMARY KEY,
    theme TEXT NOT NULL,
    text TEXT NOT NULL,
    date_text DATE NOT NULL
);

CREATE TABLE data_recognition_and_synthesis
(
    id         SERIAL PRIMARY KEY,
    client_id  INTEGER,
    text_id    INTEGER,
    recognition_data_id INTEGER,
    synthesis_data_id   INTEGER,
    sequence_number INTEGER
);

-- СВЯЗЫВАНИЕ БД ВНЕШНИМИ КЛЮЧАМИ --
ALTER TABLE data_recognition_and_synthesis
    ADD CONSTRAINT FR_data_recognition_and_synthesis_of_account
        FOREIGN KEY (text_id) REFERENCES text (id);

ALTER TABLE data_recognition_and_synthesis
    ADD CONSTRAINT FR_data_recognition_and_synthesis_of_account
        FOREIGN KEY (recognition_data_id) REFERENCES recognition_data (id);

ALTER TABLE data_recognition_and_synthesis
    ADD CONSTRAINT FR_data_recognition_and_synthesis_of_account
        FOREIGN KEY (synthesis_data_id) REFERENCES synthesis_data (id);

ALTER TABLE data_recognition_and_synthesis
    ADD CONSTRAINT FR_data_recognition_and_synthesis_of_account
        FOREIGN KEY (client_id) REFERENCES account (id);

ALTER TABLE recommendation
    ADD CONSTRAINT FR_recommendation_of_recognition_data
        FOREIGN KEY (logodedist_id) REFERENCES account (id);

ALTER TABLE recommendation
    ADD CONSTRAINT FR_recommendation_of_data_recognition_and_synthesis
        FOREIGN KEY (data_recognition_and_synthesis_id) REFERENCES data_recognition_and_synthesis (id);

-- Данные для таблицы "account"
INSERT INTO account (name, lastname, fathername, username, password, is_moderator, is_superuser, is_staff, is_active)
VALUES ('Иван', 'Иванов', 'Иванович', 'ivan_ivanov', 'password123', FALSE, FALSE, FALSE, TRUE),
       ('Петр', 'Петров', 'Петрович', 'petr_petrov', 'qwerty123', FALSE, FALSE, FALSE, TRUE),
       ('Мария', 'Сидорова', 'Сергеевна', 'maria_sidorova', 'securepass', TRUE, FALSE, FALSE, TRUE);

-- INSERT INTO account (name, lastname, fathername, username, password, is_moderator)
-- VALUES ('Иван', 'Иванов', 'Иванович', 'ivan_ivanov', 'password123', FALSE),
--        ('Петр', 'Петров', 'Петрович', 'petr_petrov', 'qwerty123', FALSE),
--        ('Мария', 'Сидорова', 'Сергеевна', 'maria_sidorova', 'securepass', TRUE);

SELECT *
FROM account;

INSERT INTO text (theme, text, date_text)
VALUES ('Погода', 'Сегодня солнечный день.', '2023-11-10'),
       ('Животные', 'Кошка сидит на окне.', '2023-11-10'),
       ('Еда', 'Я люблю яблоки.', '2023-11-10');

SELECT *
FROM text;

-- Добавление данных в таблицу recognition_data
INSERT INTO recognition_data (data_recognition, word_for_check, transcription_word, date_recoding, wer, cer, mer, wil,
                              iwer)
VALUES (E'\\xDEADBEEF', 'солнечный', 'соничный', '2023-10-26', 0.1, 0.2, 0.3, 0.4, 0.5),
       (E'\\xCAFEBABE', 'кошка', 'кошка', '2023-10-27', 0, 0, 0, 0, 0),
       (E'\\xFACEB00C', 'яблоки', 'яблоке', '2023-10-28', 0.05, 0.1, 0.05, 0.05, 0.1);

SELECT *
FROM recognition_data;

-- Добавление данных в таблицу synthesis_data
INSERT INTO synthesis_data (data_recognition, word_synthesis, word_input, date_synthesis, wer)
VALUES (E'\\xDEADBEEF', 'солнечный', 'солнышко', '2023-10-26', 0.2),
       (E'\\xCAFEBABE', 'яблоки', 'яблоко', '2023-10-28', 0.1),
       (E'\\xFACEB00C', 'кошка', 'коська', '2023-10-29', 0.1);

SELECT *
FROM synthesis_data;

-- Добавление данных в таблицу data_recognition_and_synthesis
INSERT INTO data_recognition_and_synthesis (client_id, text_id, recognition_data_id, synthesis_data_id, sequence_number)
VALUES (1, 1, 1, 1, 1),
       (2, 2, 2, 3, 1),
       (1, 3, 3, 2, 1);

SELECT *
FROM data_recognition_and_synthesis;

-- Добавление данных в таблицу recommendation
INSERT INTO recommendation (logopedist_id, data_recognition_and_synthesis_id, recommendation_type,
                            recommendation_text_by_llm, recommendation_text_by_logopedist, date_recommendation)
VALUES (3, 1, 'Произношение', 'Обратите внимание на звук "н".', 'Работайте над мягкостью звука "н".', '2023-10-27');

SELECT *
FROM recommendation;