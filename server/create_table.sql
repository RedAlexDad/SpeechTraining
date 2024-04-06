CREATE TABLE account
(
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    lastname   TEXT NOT NULL,
    fathername TEXT NOT NULL,
    username   TEXT NOT NULL,
    password   TEXT NOT NULL
);


CREATE TABLE recognition_data
(
    id                 SERIAL PRIMARY KEY,
    text               TEXT,
    transcription_text TEXT,
    date_recoding      DATE NULL,
    id_metric          INT  NULL,
    id_client          INT  NULL,
    id_recommendation  INT  NULL,
    data_recognition   VARCHAR
);

CREATE TABLE metric
(
    id   SERIAL PRIMARY KEY,
    WER  TEXT,
    CER  TEXT,
    MER  TEXT,
    WIL  TEXT,
    IWER TEXT
);

CREATE TABLE recommendation
(
    id                                SERIAL PRIMARY KEY,
    id_logodedist                     INT  NOT NULL,
    recommendation_type               TEXT,
    recommendation_text_by_llm        TEXT,
    recommendation_text_by_logopedist TEXT,
    date_recommendation               DATE NULL
);

-- СВЯЗЫВАНИЕ БД ВНЕШНИМИ КЛЮЧАМИ --
ALTER TABLE recognition_data
    ADD CONSTRAINT FR_recognition_data_of_account
        FOREIGN KEY (id_client) REFERENCES account (id);

ALTER TABLE recognition_data
    ADD CONSTRAINT FR_recognition_data_of_metric
        FOREIGN KEY (id_metric) REFERENCES metric (id);

ALTER TABLE recognition_data
    ADD CONSTRAINT FR_recognition_data_of_recommendation
        FOREIGN KEY (id_recommendation) REFERENCES recommendation (id);

ALTER TABLE recommendation
    ADD CONSTRAINT FR_recognition_data_of_recommendation
        FOREIGN KEY (id_logodedist) REFERENCES account (id);

-- Данные для таблицы "account"
INSERT INTO account (name, lastname, fathername, username, password)
VALUES ('Иван', 'Иванов', 'Иванович', 'ivan_ivanov', 'qwerty123'),
       ('Петр', 'Петров', 'Петрович', 'petr_petrov', 'password123'),
       ('Мария', 'Сидорова', 'Игоревна', 'maria_sidorova', 'securepassword');

SELECT *
FROM account;

-- Данные для таблицы "metric"
INSERT INTO metric (WER, CER, MER, WIL, IWER)
VALUES ('0.1', '0.05', '0.08', '0.03', '0.12'),
       ('0.15', '0.07', '0.1', '0.04', '0.17'),
       ('0.09', '0.04', '0.06', '0.02', '0.1');

SELECT *
FROM metric;

INSERT INTO recommendation (id_logodedist, recommendation_type, recommendation_text_by_llm,
                            recommendation_text_by_logopedist, date_recommendation)
VALUES (1, 'Улучшение', 'Неплохо, продолжай в том же духе', 'На основе LLM я согласен с выводом', '2023-05-04'),
       (2, 'Устранение', 'Проблема с произношением Р', 'Попробуйте расположить язык на небе', '2023-05-04'),
       (3, 'Улучшение', 'Неплохо, продолжай в том же духе. Проговаривайте', 'Попробуйте расположить язык на небе',
        '2023-05-04');

SELECT *
FROM recommendation;

-- Данные для таблицы "recognition_data"
INSERT INTO recognition_data (id_client, text, date_recoding, transcription_text, id_metric,
                                       id_recommendation)
VALUES (1, 'Привет, как дела?', '2023-11-04', 'Привет, как дела?', 1, 1),
       (2, 'Это тестовая фраза.', '2023-12-04', 'Это тестовая фраза.', 2, 2),
       (3, 'Опять проверяем работу.', '2023-05-04', 'Опять проверяем работу.', 3, 3);

SELECT *
FROM recognition_data;

