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

        print("Преобразация аудиофайла в формате ogg с частотой дидискретизации 16000 Гц.")
        # Преобразование в нужный формат
        audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        audio.export("test.ogg", format="ogg")
        print(f"Аудиофайл преобразован и сохранен как '{file_path}'.")

    if audio.channels > 1:
        print("Максимальное количество аудиоканалов — 1.")

if __name__ == "__main__":
    print('-' * 50)
    file_path = 'voice/'
    record_audio = ['ai.ogg', 'speechkit-ogg.ogg', 'hello_world.ogg', 'test.ogg', 'output.ogg']

    for file_name in record_audio:
        print(f"Запись аудиофайла:  {file_name}")
        file = file_path + file_name
        print_audio_info(file)
        print('-' * 50)
