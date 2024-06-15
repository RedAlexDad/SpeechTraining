import os
import sys
import pyaudio
import wave
import uuid

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QTextEdit
from PyQt5.QtCore import QTimer

from sentences_text import sentences_text


class AudioRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 350

        # Предложения
        self.sentences_text = sentences_text
        self.current_sentence_index = 0
        self.topic_combobox = QComboBox(self)
        self.topic_combobox.setPlaceholderText("Выберите тему")
        self.topic_combobox.addItems(sentences_text.keys())
        self.topic_combobox.currentIndexChanged.connect(self.update_text)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.update_text()  # Обновление текста при запуске

        # Таймер записи
        self.timer = QTimer(self)
        self.time_elapsed = 0

        self.initUI()
        self.setup_audio()

    def initUI(self):
        self.setWindowTitle("Запись звука")
        self.setGeometry(100, 100, self.width, self.height)  # Установка размера окна 400х300

        self.sentence_label = QLabel(self)
        self.sentence_label.setWordWrap(True)

        self.start_button = QPushButton("Начать запись", self)
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton("Остановить запись", self)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)

        self.timer.timeout.connect(self.update_timer)
        self.time_label = QLabel("Время: 00:00", self)

        layout = QVBoxLayout()
        layout.addWidget(self.topic_combobox)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.time_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)
        self.setFixedSize(self.width, self.height)  # Фиксация размера окна

    def update_timer(self):
        self.time_elapsed += 1
        minutes = self.time_elapsed // 60
        seconds = self.time_elapsed % 60
        self.time_label.setText(f"Время: {minutes:02}:{seconds:02}")

    def update_text(self):
        selected_topic = self.topic_combobox.currentText()
        selected_text = sentences_text.get(selected_topic, "Текст не найден")
        self.text_edit.setPlainText(selected_text)

    def setup_audio(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.WAVE_OUTPUT_FILENAME = "../voice/output.ogg"

        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.recording = False

    def start_recording(self):
        self.time_elapsed = 0
        self.timer.start(1000)

        self.recording = True
        self.frames = []
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.record_audio()

    def record_audio(self):
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            QApplication.processEvents()  # Обработка событий GUI

    def stop_recording(self):
        self.timer.stop()
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.save_recording()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def save_recording(self):
        output_dir = '../voice'
        os.makedirs(output_dir, exist_ok=True)  # Создаем каталог, если он не существует

        waveFile = wave.open(os.path.join(output_dir, 'output.ogg'), 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(self.frames))
        waveFile.close()

    def next_sentence(self):
        self.current_sentence_index = (self.current_sentence_index + 1) % len(self.sentences)
        self.sentence_label.setText(self.sentences[self.current_sentence_index])

    def closeEvent(self, event):
        self.audio.terminate()
        event.accept()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     recorder = AudioRecorder()
#     recorder.show()
#     sys.exit(app.exec_())
