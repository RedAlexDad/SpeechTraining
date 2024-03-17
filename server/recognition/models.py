from django.db import models

class Transcription(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(null=False)
    transcription_text = models.TextField(null=True)
    wer = models.IntegerField(null=True)
    cer = models.IntegerField(null=True)
    mer = models.IntegerField(null=True)
    wil = models.IntegerField(null=True)