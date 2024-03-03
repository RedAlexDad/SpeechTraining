import os
import shutil

# Путь к основному каталогу
base_path = "/home/redalexdad/recognition_speech/buriy_audiobooks_2_val"

def create_directories_and_move_files(current_path):
    # Получаем список элементов в текущем каталоге
    elements = os.listdir(current_path)

    # Проходим по каждому элементу
    for element in elements:
        element_path = os.path.join(current_path, element)

        # Проверяем, является ли элемент каталогом
        if os.path.isdir(element_path):
            # Рекурсивно вызываем функцию для обработки вложенного каталога
            create_directories_and_move_files(element_path)
        else:
            # Проверяем, является ли файл текстовым файлом
            if element.endswith(".txt"):
                # Читаем содержимое текстового файла
                with open(element_path, 'r') as txt_file:
                    folder_name = txt_file.read().strip()

                # Формируем новый путь для создания каталога
                new_folder_path = os.path.join(current_path, folder_name)

                # Создаем каталог, если он не существует
                if not os.path.exists(new_folder_path):
                    os.makedirs(new_folder_path)

                # Формируем новый путь для перемещения файла
                new_file_path = os.path.join(new_folder_path, element.replace(".txt", ".wav"))

                # Перемещаем файл в новый каталог
                shutil.move(element_path, new_file_path)

                print(f"Каталог {folder_name} создан, файл перемещен.")


# Вызываем функцию для выполнения операций
create_directories_and_move_files()