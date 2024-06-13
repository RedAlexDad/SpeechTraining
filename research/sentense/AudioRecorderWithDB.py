import io
import wave
import tempfile
import subprocess

import numpy as np
import soundfile as sf

from research.sentense.AudioRecorderGUI import AudioRecorder
from research.sentense.DB_PostgreSQL import AudioRecorderDB
from research.sentense.AutomaticSpeechRecognitionrYandex import AutomaticSpeechRecognitionYandex

class AudioRecorderWithDB(AudioRecorder):
    def __init__(self, FOLDER_ID, IAM_TOKEN):
        super().__init__()
        self.db = AudioRecorderDB(dbname='asr_text', user='postgres', password='postgres', host='localhost', port='5432')
        self.db.connect()
        self.automatic_speech_recognizer = AutomaticSpeechRecognitionYandex(FOLDER_ID, IAM_TOKEN)

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
                transcript_text = self.automatic_speech_recognizer.recognize_speech_audio_data(voice_recording)
                self.db.insert_record(topic, paragraph_text, transcript_text, voice_recording)

        # Вызов метода родительского класса для сохранения аудиофайла на диск
        # super().save_recording()

    def closeEvent(self, event):
        self.db.disconnect()
        super().closeEvent(event)
