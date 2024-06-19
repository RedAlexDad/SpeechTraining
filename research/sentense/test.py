import pyaudio

class AudioRecorder:
    def __init__(self):
        self.setup_audio()

    def setup_audio(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.WAVE_OUTPUT_FILENAME = "../voice/output.ogg"

        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.recording = False

    def get_input_device_index(self):
        for i in range(self.audio.get_device_count()):
            dev = self.audio.get_device_info_by_index(i)
            if dev['maxInputChannels'] > 0:
                print(f"Устройство: {dev['name']}, Индекс: {i}, Частота: {dev['defaultSampleRate']}")
                if 'supportedSampleRates' in dev and self.RATE in dev['supportedSampleRates']:
                    return i
        raise ValueError("Не удалось найти подходящее входное устройство.")

    def start_recording(self):
        self.time_elapsed = 0

        self.recording = True
        self.frames = []
        self.input_device_index = self.get_input_device_index()  # Установите здесь нужный индекс устройства
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=self.input_device_index,
            frames_per_buffer=self.CHUNK
        )
        self.record_audio()

    def record_audio(self):
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

# Пример использования
if __name__ == "__main__":
    audio_recorder = AudioRecorder()
    audio_recorder.start_recording()
