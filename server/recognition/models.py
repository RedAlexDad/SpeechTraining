from django.db import models

class Transcription(models.Model):
    text = models.TextField()
    transcription_text = models.TextField()
    error_percentage = models.TextField()
