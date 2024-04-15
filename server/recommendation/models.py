from django.db import models
from account.models import Account
from async_transcription_and_speech_synthesis.models import DataRecognitionAndSynthesis


class Recommendation(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    logopedist = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Логопед",
                                   limit_choices_to={'is_moderator': True})
    data_recognition_and_synthesis = models.ForeignKey(DataRecognitionAndSynthesis, on_delete=models.CASCADE,
                                                       verbose_name="Данные распознавания и синтеза")
    recommendation_type = models.TextField(null=True, verbose_name="Тип рекомендации")
    recommendation_text_by_llm = models.TextField(null=True, verbose_name="Текст рекомендации (LLM)")
    recommendation_text_by_logopedist = models.TextField(null=True, verbose_name="Текст рекомендации (логопед)")
    date_recommendation = models.DateField(null=True, verbose_name="Дата рекомендации")

    class Meta:
        db_table = 'recommendation'
        verbose_name = "Рекомендация"
