import io
import wave
import tempfile
import subprocess

import numpy as np
import soundfile as sf

from research.sentense.AudioRecorderGUI import AudioRecorder
from research.sentense.DB_PostgreSQL import AudioRecorderDB
from research.sentense.AutomaticSpeechRecognitionYandex import AutomaticSpeechRecognitionYandex
from research.sentense.AutomaticSpeechRecognitionMBART50 import AutomaticSpeechRecognitionMBART50
from research.sentense.AutomaticSpeechRecognitionSaluteSpeech import AutomaticSpeechRecognitionSaluteSpeech


class AudioRecorderWithDB(AudioRecorder):
    def __init__(self, FOLDER_ID_Y, OAUTH, CLINET_ID_S, CLIENT_SECRET_S):
        super().__init__()
        self.db = AudioRecorderDB(dbname='asr_text', user='postgres', password='postgres', host='localhost',
                                  port='5432')
        self.db.connect()
        self.asr_yandex = AutomaticSpeechRecognitionYandex(FOLDER_ID_Y, OAUTH)
        self.asr_mbart50 = AutomaticSpeechRecognitionMBART50()
        self.asr_salute_speech = AutomaticSpeechRecognitionSaluteSpeech(CLINET_ID_S, CLIENT_SECRET_S)

    def save_recording(self):
        # Создание временного файла для сохранения записанных аудиоданных
        with tempfile.NamedTemporaryFile(suffix='.wav') as temp_file:
            # Преобразование аудиоданных в формат 'int16' для записи с помощью soundfile
            frames_np = np.frombuffer(b''.join(self.frames), dtype=np.int16)

            # Запись аудиоданных во временный файл
            with sf.SoundFile(temp_file.name, mode='w', samplerate=self.RATE, channels=self.CHANNELS, format='WAV',
                              subtype='PCM_16') as f:
                f.write(frames_np)

            # Преобразование формата аудиофайла в OggOpus с помощью ffmpeg
            with tempfile.TemporaryFile(suffix='.ogg') as buffer:
                subprocess.run(['ffmpeg', '-i', temp_file.name, '-f', 'ogg', '-acodec', 'libopus', '-'], stdout=buffer)
                buffer.seek(0)
                voice_recording = buffer.read()

            # Сохранение записи в базе данных
            if self.frames:
                topic = self.topic_combobox.currentText()
                paragraph_text = self.text_edit.toPlainText()
                transcript_text_yandex = self.asr_yandex.recognize_speech_audio_data(voice_recording)
                transcript_text_salutespeech = self.asr_salute_speech.recognize_speech_salute(voice_recording)
                transcript_text_mbart50 = self.asr_mbart50.transcribe_audio(frames_np)
                self.db.insert_record(
                    topic=topic,
                    paragraph_text=paragraph_text,
                    transcript_text_yandex=transcript_text_yandex,
                    transcript_text_salutespeech=transcript_text_salutespeech,
                    transcript_text_mbart50=transcript_text_mbart50,
                    voice_recording=voice_recording
                )

        # Вызов метода родительского класса для сохранения аудиофайла на диск
        super().save_recording()

    def closeEvent(self, event):
        self.db.disconnect()
        super().closeEvent(event)
