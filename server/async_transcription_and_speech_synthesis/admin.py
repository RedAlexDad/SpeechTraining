from django.contrib import admin
from async_transcription_and_speech_synthesis.models import RecognitionData, DataRecognitionAndSynthesis, SynthesisData

admin.site.register(RecognitionData)
admin.site.register(DataRecognitionAndSynthesis)
admin.site.register(SynthesisData)
