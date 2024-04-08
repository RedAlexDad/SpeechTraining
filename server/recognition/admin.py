from django.contrib import admin
from .models import Account, DataRecognitionAndSynthesis, RecognitionData, SynthesisData, Recommendation

admin.site.register(Account)
admin.site.register(DataRecognitionAndSynthesis)
admin.site.register(SynthesisData)
admin.site.register(RecognitionData)
admin.site.register(Recommendation)
