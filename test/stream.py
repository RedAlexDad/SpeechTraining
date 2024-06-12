import pyaudio
import wave
import speech_recognition as sr

def record_audio(filename, duration):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = duration

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Запись аудио...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* Запись завершена.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def recognize_speech(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)

    try:
        print("Вы сказали: " + recognizer.recognize_google(audio_data, language="ru-RU"))
    except sr.UnknownValueError:
        print("Извините, не удалось распознать речь")
    except sr.RequestError as e:
        print("Ошибка сервиса распознавания: {0}".format(e))

if __name__ == "__main__":
    filename = input("Введите имя файла для записи: ")
    duration = int(input("Введите длительность записи в секундах: "))

    record_audio(filename, duration)
    print("Аудио сохранено в файле", filename)

    print("Начинаем распознавание речи...")
    recognize_speech(filename)
