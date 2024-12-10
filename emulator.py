import xml.etree.ElementTree as ET
import tarfile
import os
import time

# Функция для чтения конфигурации из XML
def parse_config(xml_file):
    tree = ET.parse(xml_file)  # Парсим XML файл
    root = tree.getroot()  # Получаем корень XML
    
    # Извлекаем значения из тегов
    username = root.find('username').text
    computername = root.find('computername').text
    filesystem = root.find('filesystem').text

    return username, computername, filesystem

# Функция для отображения командной строки
def shell_prompt(username, computername, current_directory):
    return f"{username}@{computername} {current_directory} $ "

# Функция для выполнения команд в эмуляторе
def run_shell(username, computername, filesystem):
    current_directory = "/"  # Начинаем с корневой директории
    start_time = time.time()  # Засекаем время начала работы программы

    while True:
        command = input(shell_prompt(username, computername, current_directory))  # Запрос на ввод команды

        if command == "exit":
            print("Exiting...")  # Завершаем программу
            break
        elif command == "ls":
            files = list_files_in_tar(filesystem, current_directory)  # Получаем список файлов из .tar архива
            print("\n".join(files))  # Печатаем их
        elif command.startswith("cd "):
            dir_to_cd = command.split(" ")[1]  # Извлекаем имя директории
            current_directory = change_directory(filesystem, current_directory, dir_to_cd)  # Меняем директорию
        elif command == "pwd":
            print(current_directory)  # Печатаем текущую директорию
        elif command == "uptime":
            uptime_seconds = time.time() - start_time  # Считаем время работы
            print(f"Uptime: {uptime_seconds:.2f} seconds")
        elif command.startswith("tac "):
            file_to_read = command.split(" ")[1]  # Извлекаем имя файла
            tac_file(filesystem, current_directory, file_to_read)  # Выводим содержимое файла в обратном порядке
        else:
            print(f"Command '{command}' not found.")  # Если команда неизвестна

# Функция для получения списка файлов из архива .tar
def list_files_in_tar(tar_path, current_directory):
    try:
        with tarfile.open(tar_path, 'r') as tar:  # Открываем .tar архив
            # Получаем все файлы в архиве
            files = tar.getnames()
            # Фильтруем файлы, которые находятся в текущей директории
            current_dir_prefix = current_directory.strip("/") + "/" if current_directory != "/" else ""
            filtered_files = [f[len(current_dir_prefix):] for f in files if f.startswith(current_dir_prefix)]
            # Возвращаем только файлы и директории на одном уровне
            return sorted(set([f.split("/")[0] for f in filtered_files]))
    except Exception as e:
        print(f"Error reading tar file: {e}")
        return []

# Функция для изменения директории в архиве
def change_directory(tar_path, current_directory, dir_to_cd):
    try:
        # Если команда "cd /", возвращаем корень
        if dir_to_cd == "/":
            return "/"
        
        # Если команда "cd ..", возвращаем на уровень выше
        if dir_to_cd == "..":
            # Если в корне, остаемся там
            if current_directory == "/":
                return "/"
            # Убираем последний уровень
            return "/" + "/".join(current_directory.strip("/").split("/")[:-1])
        
        with tarfile.open(tar_path, 'r') as tar:
            # Получаем все файлы в архиве
            files = tar.getnames()
            # Формируем новый путь
            new_directory = os.path.join(current_directory, dir_to_cd).strip("/")
            # Проверяем, существует ли директория
            if any(f.startswith(new_directory + "/") for f in files):
                return "/" + new_directory  # Переход в новую директорию
            else:
                print(f"Directory '{dir_to_cd}' not found.")
                return current_directory  # Остаемся в текущей директории
    except Exception as e:
        print(f"Error accessing tar file: {e}")
        return current_directory

# Функция для вывода содержимого файла в обратном порядке
def tac_file(tar_path, current_directory, file_name):
    try:
        with tarfile.open(tar_path, 'r') as tar:  # Открываем .tar архив
            file_path = os.path.join(current_directory.strip("/"), file_name).strip("/")
            try:
                file_content = tar.extractfile(file_path).read().decode('utf-8')  # Читаем содержимое файла
                lines = file_content.splitlines()  # Разделяем на строки
                for line in reversed(lines):  # Печатаем строки в обратном порядке
                    print(line)
            except KeyError:
                print(f"File '{file_name}' not found.")
    except Exception as e:
        print(f"Error accessing tar file: {e}")

if __name__ == "__main__":
    config_file = "config.xml"  # Указываем путь к конфигу
    username, computername, filesystem = parse_config(config_file)  # Извлекаем данные из конфиг файла
    run_shell(username, computername, filesystem)  # Запускаем командную оболочку
