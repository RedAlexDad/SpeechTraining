from rest_framework import serializers
from async_transcription_and_speech_synthesis.models import DataRecognitionAndSynthesis, RecognitionData, SynthesisData, Text

class RecognitionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognitionData
        fields = '__all__'


class DataRecognitionAndSynthesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRecognitionAndSynthesis
        fields = '__all__'


class SynthesisDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynthesisData
        fields = '__all__'


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'