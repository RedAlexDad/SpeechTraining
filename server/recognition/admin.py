from django.contrib import admin
from .models import Account, Recommendation, Metrics, RecognitionData

admin.site.register(Account)
admin.site.register(Recommendation)
admin.site.register(Metrics)
admin.site.register(RecognitionData)