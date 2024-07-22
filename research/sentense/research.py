# Импорт библиотеки
import sys
import os
import re
import numpy as np
from jiwer import wer, cer, mer, wil, compute_measures

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Функция для подсчета расстояния Левенштейна
def levenshtein_distance(a, b):
    m, n = len(a), len(b)
    dp = np.zeros((m + 1, n + 1), dtype=int)

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,  # удаление
                               dp[i][j - 1] + 1,  # вставка
                               dp[i - 1][j - 1] + 1)  # замена
    return dp[m][n]


# Тексты
reference = "Искусственный интеллект (ИИ) - это область компьютерных наук, создающая системы для выполнения задач, требующих человеческого интеллекта: распознавание речи, обработка изображений, принятие решений. Искусственный интеллект проникает во все сферы жизни, от рекомендаций в онлайн-магазинах до медицинских диагнозов."
# recognized = "Искусственный интеллект (ИИ) - это область компьютерных наук, создающая системы для выполнения задач, требующих человеческого интеллекта: распознавание речи, обработка изображений, принятие решений. Искусственный интеллект проникает во все сферы жизни, от рекомендаций в онлайн-магазинах до медицинских диагнозов."
# recognized = "Искусственный test (ИИ) - test область компьютерных наук, создающая системы для выполнения задач, требующих человеческого интеллекта: распознавание речи, обработка изображений, принятие решений. Искусственный интеллект проникает во все сферы жизни, от рекомендаций в онлайн-магазинах до медицинских диагнозов."
# recognized = "Существует интеллект это вопрос от компьютерных наук состоящий из системы для повышения сдачи требующей человеческого интеллекта распознавания речи о пропатке изображения принятие решений а искусство не интеллект проникает во все сферы жизни от рекомендуется магазинах"
recognized = "Рвотчины технари мнящие мир и проносящие на четверни двигатель барылочных опрашивает однако я выражаю это и вызывают Аспектами будущими исследования и разработки в вопросе Проект путь играть ключевую роль в формировании общества и экономики"
# recognized = "Аваывыа"

# Разделение на слова
ref_words = reference.split()
rec_words = recognized.split()

# Вычисление MER для каждого слова
mer_per_word = []

for ref_word in ref_words:
    min_distance = float('inf')
    for rec_word in rec_words:
        distance = levenshtein_distance(ref_word, rec_word)
        if distance < min_distance:
            min_distance = distance
    mer_per_word.append(min_distance / len(ref_word))

print(f'Вариант №1 - Расстояние Левенштейна: {np.mean(mer_per_word)}')

# Функция для вычисления MER по каждому слову
def calculate_mer_per_word(ref_words, rec_words):
    mer_per_word = []
    for ref_word in ref_words:
        ref_text = ref_word
        rec_text = ' '.join(rec_words)
        word_mer = mer([ref_text], [rec_text])
        mer_per_word.append(word_mer)
    return mer_per_word

# Вычисление MER по каждому слову
mer_per_word = calculate_mer_per_word(ref_words, rec_words)
print(f'Вариант №2 - Вычисления MER по каждому слову: {np.mean(mer_per_word)}')


# Функция для вычисления MER по каждому слову
def calculate_mer_per_word(ref_words, rec_words):
    mer_per_word = []
    for i, ref_word in enumerate(ref_words):
        if i < len(rec_words):
            rec_word = rec_words[i]
        else:
            rec_word = ""
        measures = compute_measures(ref_word, rec_word)
        word_mer = measures['mer']
        mer_per_word.append(word_mer)
    return mer_per_word

# Вычисление MER по каждому слову
mer_per_word = calculate_mer_per_word(ref_words, rec_words)
print(f'Вариант №3: {np.mean(mer_per_word)}')
