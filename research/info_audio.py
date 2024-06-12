from pydub import AudioSegment


def print_audio_info(file_path):
    audio = AudioSegment.from_file(file_path)
    print(f"Длина аудиофайла: {len(audio) / 1000} секунд")
    print(f"Частота дискретизации: {audio.frame_rate} Гц")
    print(f"Количество каналов: {audio.channels}")
    print(f"Ширина выборки: {audio.sample_width} байт")

    if len(audio) > 30000:
        print("Аудиофайл превышает максимальную длительность 30 секунд.")
    if audio.frame_rate not in [8000, 16000]:
        print("Частота дискретизации должна быть 8000 или 16000 Гц.")
    if audio.channels > 1:
        print("Максимальное количество аудиоканалов — 1.")

    # Преобразование в нужный формат
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    audio.export("test.ogg", format="ogg")
    print(f"Аудиофайл преобразован и сохранен как '{file_path}'.")


if __name__ == "__main__":
    print('-' * 50)
    file_path = '../voice/'
    # record_audio = [file_path + 'ai.ogg', file_path + 'speechkit-ogg.ogg']
    # record_audio = [file_path + 'ai.ogg']
    record_audio = [file_path + 'test.ogg']

    for file in record_audio:
        print_audio_info(file)
        print('-' * 50)
