#!/bin/bash
# Этот файл должен находиться в то место, где оттуда данные берутся

# Путь к основному каталогу, от которого будет копировать новые каталоги и файлы
base_path="/home/redalexdad/recognition_speech/buriy_audiobooks_2_val"

# Перебор всех текстовых файлов в основном каталоге
find "$base_path" -type f -name "*.txt" | while read -r txt_file; do
    # Проверка наличия текстового файла
    if [ -e "$txt_file" ]; then
        # Чтение содержимого текстового файла
        folder_name=$(cat "$txt_file")

        # Формирование нового пути для каталога в новой директории
        new_folder_path="/home/redalexdad/recognition_speech/new_buriy_audiobooks_2_val/$folder_name"

        # Создание нового каталога, если его еще нет
        mkdir -p "$new_folder_path"

        # Получаем имя аудиофайла без полного пути
        audio_file=$(basename "${txt_file%.txt}.wav")

        # Перемещение аудиофайла в новый каталог
        mv "${txt_file%.txt}.wav" "$new_folder_path/$audio_file"
		
        # Перемещение текстового файла в новый каталог
        mv "$txt_file" "$new_folder_path/${txt_file##*/}"

       echo "Каталог \"$folder_name\" создан, аудиофайл и текстовый файл перемещены."
    else
        echo "Ошибка: Текстовый файл \"$txt_file\" не найден."
    fi
done