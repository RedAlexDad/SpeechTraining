from django.db import models
from account.models import Account

class RecognitionData(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    data_recognition = models.BinaryField(null=True, verbose_name="Запись голоса")
    word_for_check = models.TextField(null=True, verbose_name="Слово для проверки")
    transcription_word = models.TextField(null=True, verbose_name="Слово транскрибации")
    date_recoding = models.DateField(null=True, verbose_name="Дата записи")
    wer = models.FloatField(null=True, verbose_name="WER")
    cer = models.FloatField(null=True, verbose_name="CER")
    mer = models.FloatField(null=True, verbose_name="MER")
    wil = models.FloatField(null=True, verbose_name="WIL")
    iwer = models.FloatField(null=True, verbose_name="IWER")

    class Meta:
        db_table = 'recognition_data'
        verbose_name = "Распознавание речи"


class SynthesisData(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    data_recognition = models.BinaryField(null=True, verbose_name="Синтез речи")
    word_synthesis = models.TextField(null=True, verbose_name="Слово синтеза")
    word_input = models.TextField(null=True, verbose_name="Введенное слово")
    date_synthesis = models.DateField(null=True, verbose_name="Дата синтеза")
    wer = models.FloatField(null=True, verbose_name="WER")

    class Meta:
        db_table = 'synthesis_data'
        verbose_name = "Синтез речи"


class Text(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    theme = models.TextField(verbose_name="Тема")
    text = models.TextField(verbose_name="Текст")
    date_text = models.DateField(verbose_name="Дата текста")

    class Meta:
        db_table = 'text'
        verbose_name = "Текст"

class DataRecognitionAndSynthesis(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    client = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Клиент")
    text = models.ForeignKey(Text, on_delete=models.CASCADE, verbose_name="Текст")
    recognition_data = models.ForeignKey(RecognitionData, on_delete=models.CASCADE, verbose_name="Данные распознавания",
                                         null=True, blank=True)
    synthesis_data = models.ForeignKey(SynthesisData, on_delete=models.CASCADE, verbose_name="Данные синтеза",
                                       null=True, blank=True)
    sequence_number = models.IntegerField(verbose_name="Порядковый номер")

    class Meta:
        db_table = 'data_recognition_and_synthesis'
        verbose_name = "Данные распознавания и синтеза речи"

