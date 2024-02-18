from transformers import AutoTokenizer, Wav2Vec2ForCTC
import torch
import torchaudio
import jiwer
import sounddevice as sd
import time

# Загрузка модели и токенизатора
tokenizer = AutoTokenizer.from_pretrained(
    "Edresson/wav2vec2-large-100k-voxpopuli-ft-Common-Voice_plus_TTS-Dataset-russian")
model = Wav2Vec2ForCTC.from_pretrained(
    "Edresson/wav2vec2-large-100k-voxpopuli-ft-Common-Voice_plus_TTS-Dataset-russian")

# Ваш код для загрузки и обработки субтитров
# Например, вы можете использовать библиотеку jiwer для вычисления Word Error Rate (WER)
# Убедитесь, что у вас есть правильные субтитры для сравнения
reference_text = "тестирование пройдено успешно"


def record_and_transcribe():
    while True:
        # Запись звука
        print('Начало записи звука')
        # Запись голоса и сохранение в формате WAV
        recording = sd.rec(int(3 * 44100), samplerate=44100, channels=1, dtype='int16')
        sd.wait()
        # Преобразуем 1D тензор в 2D, добавив размерность пакета
        recording = torch.from_numpy(recording.squeeze()).unsqueeze(0)
        torchaudio.save("voice/recorded_audio.wav", recording, 44100)
        print('Конец записи звука')

        # Загрузка записанного аудиофайла
        audio_path = "./voice/recorded_audio.wav"
        speech, _ = torchaudio.load(audio_path)

        # Преобразование с использованием модели
        resampler = torchaudio.transforms.Resample(orig_freq=48_000, new_freq=16_000)
        input_values = resampler.forward(speech.squeeze(0)).numpy()

        # Токенизация и получение предсказания от модели
        input_values = torch.tensor(input_values).unsqueeze(0)  # добавляем размерность пакета
        with torch.no_grad():
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)

        # Декодирование предсказанных токенов в текст
        transcription = tokenizer.batch_decode(predicted_ids)[0]

        # Вывод результата на консоль
        print("Распознанный текст:", transcription)

        # Пауза на 3 секунды
        time.sleep(2)

# Запуск функции записи и распознавания
record_and_transcribe()
