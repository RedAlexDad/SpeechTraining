from jiwer import wer, cer, mer, wil


class Metrics:
    def __init__(self):
        self.wer_score = None
        self.cer_score = None
        self.mer_score = None
        self.wil_score = None
        self.iwer_score = None

    # Функция проверки всех метрик
    def calculate_metrics(self, reference_text, transcription_text) -> tuple[float, float, float, float, float]:
        # Подсчет WER
        self.wer_score = wer(reference_text, transcription_text)
        # Подсчет CER
        self.cer_score = cer(reference_text, transcription_text)
        # Подсчет MER
        self.mer_score = mer(reference_text, transcription_text)
        # Подсчет WIL
        self.wil_score = wil(reference_text, transcription_text)
        # По
        self.iwer_score = 1 - self.iwer(reference_text, transcription_text)

        print(f"WER: {self.wer_score:.2f}, ", f"CER: {self.cer_score:.2f}, ", f"MER: {self.mer_score:.2f}, ",
              f"WIL: {self.wil_score:.2f}, ", f"IWER: {self.iwer_score:.2f};")

        return self.wer_score, self.cer_score, self.mer_score, self.wil_score, self.iwer_score

    def iwer(self, reference_sentence, hypothesis_sentence) -> float:
        """
        Вычисляет Inflectional Word Error Rate (IWER) между предложением-эталоном и гипотезой.

        Параметры:
        reference_sentence (str): Предложение-эталон (правильный вариант).
        hypothesis_sentence (str): Гипотеза (предсказанный вариант).

        Возвращает:
        float: Значение Inflectional Word Error Rate (IWER) в процентах.
        """
        reference_words = reference_sentence.split()
        hypothesis_words = hypothesis_sentence.split()

        # Находим количество слов в предложении-эталоне
        total_words = len(reference_words)

        # Считаем количество неправильно распознанных слов
        incorrect_words = sum(1 for ref, hyp in zip(reference_words, hypothesis_words) if ref != hyp)

        # Вычисляем Inflectional Word Error Rate (IWER)
        iwer_score = incorrect_words / total_words

        return iwer_score
