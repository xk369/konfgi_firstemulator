<img width="857" alt="image" src="https://github.com/user-attachments/assets/d6de10ec-bc2e-49e4-9b2b-e51e29501271">Вариант №13

Задание №1

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме CLI.
Конфигурационный файл имеет формат xml и содержит:
• Имя пользователя для показа в приглашении к вводу.
• Имя компьютера для показа в приглашении к вводу.
• Путь к архиву виртуальной файловой системы.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:
1. uptime.
2. tac.
Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 2 теста.


<img width="857" alt="image" src="https://github.com/user-attachments/assets/c99c4c0b-0ffa-4dec-9795-2b139f13c328">


## команда запуска теста
```
python3 -m unittest discover -v tests
```

<img width="857" alt="image" src="https://github.com/user-attachments/assets/6188c417-0d1f-43ec-84d9-3ab743871d54">



