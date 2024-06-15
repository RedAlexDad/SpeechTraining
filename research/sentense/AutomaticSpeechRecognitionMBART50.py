import os
import numpy as np
import torch
import soundfile as sf
import librosa
from transformers import SpeechEncoderDecoderModel, Wav2Vec2Processor

class AutomaticSpeechRecognitionMBART50:
    def __init__(self, run_model=True):
        # Использование CPU для предсказания модели
        self.device = 'cpu'
        # Запуск модели (несколько времени занимает)
        self.connect_model() if run_model else setattr(self, 'connect_model', None)

    def connect_model(self):
        self.NUM_PROCESSES = max(4, os.cpu_count())  # Количество потоков для обучения и предсказния
        self.LANG_ID = 'ru'  # Русский язык
        self.MODEL_ID = 'bond005/wav2vec2-mbart50-ru'  # Название модели
        self.PATH_MODEL = '/home/redalexdad/recognition_speech/wav2vec2-mbart50-ru'  # Путь до модели

        if os.path.exists(self.PATH_MODEL):
            self.processor = Wav2Vec2Processor.from_pretrained(self.PATH_MODEL)
            self.model = SpeechEncoderDecoderModel.from_pretrained(self.PATH_MODEL).to(self.device)
            print('Модель успешно загружена')
        else:
            self.processor = Wav2Vec2Processor.from_pretrained(self.MODEL_ID)
            self.processor.save_pretrained(self.PATH_MODEL)
            self.model = SpeechEncoderDecoderModel.from_pretrained(self.MODEL_ID).to(self.device)
            self.model.save_pretrained(self.PATH_MODEL)
            print(f'Модель успешно загружена и сохранена в {self.PATH_MODEL}')

    def transcribe_audio(self, audio_data):
        try:
            audio_tensor = torch.FloatTensor(audio_data.squeeze()).to(self.device)
            processed = self.processor(audio_tensor, sampling_rate=16000, return_tensors="pt", padding='longest').to(
                self.device)
            with torch.no_grad():
                predicted_ids = self.model.generate(**processed).to(self.device)
                transcription = self.processor.batch_decode(
                    predicted_ids,
                    num_processes=self.NUM_PROCESSES,
                    skip_special_tokens=True
                )[0]
                print('[MBART50] Распознанный текст:', transcription)
                return transcription.lower()
        except Exception as e:
            print(f"Ошибка транскрибации аудио: {e}")
            return 'None'

    def load_audio(self, file_path):
        try:
            audio_data, sample_rate = sf.read(file_path)
            if sample_rate != 16000:
                print("Частота дискретизации аудио должна быть 16000 Гц. Изменен аудиофайл на 16000 Гц.")
                audio_data = librosa.resample(audio_data, orig_sr=sample_rate, target_sr=16000)
            return audio_data
        except Exception as e:
            print(f"Ошибка загрузки аудио файла: {e}")
            return None

#
# if __name__ == '__main__':
#     ASR = AutomaticSpeechRecognitionMBART50()
#
#     # Укажите путь к вашему аудиофайлу
#     audio_file_path = '../voice/ai.ogg'
#
#     # Загрузка аудиофайла
#     audio_data = ASR.load_audio(audio_file_path)
#
#     # Распознавание речи, если аудиофайл успешно загружен
#     if audio_data is not None:
#         transcription = ASR.transcribe_audio(audio_data)
#         if transcription:
#             print("Распознанный текст:", transcription)
#         else:
#             print("Не удалось распознать текст")
