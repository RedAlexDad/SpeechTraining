import pyaudio
import wave
import tkinter as tk
from threading import Thread

# Параметры аудиозаписи
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "../trainer_text/output.ogg"

# Инициализация PyAudio
audio = pyaudio.PyAudio()
frames = []

# Флаг для остановки записи
recording = False

def start_recording():
    global recording, frames
    recording = True
    frames = []
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    save_recording()

def save_recording():
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def stop_recording():
    global recording
    recording = False

def start_recording_thread():
    thread = Thread(target=start_recording)
    thread.start()

# Создание интерфейса с кнопкой
root = tk.Tk()
root.title("Запись звука")

start_button = tk.Button(root, text="Начать запись", command=start_recording_thread)
start_button.pack(pady=20)

stop_button = tk.Button(root, text="Остановить запись", command=stop_recording)
stop_button.pack(pady=20)

root.mainloop()

# Завершение PyAudio
audio.terminate()
