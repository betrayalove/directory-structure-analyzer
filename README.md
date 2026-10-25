# Анализатор структуры директорий

**Простой и удобный инструмент для визуализации и копирования структуры любой папки. Поддерживает русский и английский интерфейс. Разработан на PyQt5.**

---

## Возможности
- Визуальное дерево директорий с кликабельными файлами
- Копирование содержимого файла в буфер обмена
- Гибкая фильтрация (скрытые, системные, с точкой, со спецсимволами, по шаблонам)
- Переключение языка (русский/английский)
- Настраиваемая глубина и отступ
- Не требует интернета, не создает скрытых процессов

## Скриншот
*(Добавьте сюда скриншот приложения)*

## Установка
1. Установите Python 3.8+
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Сборка EXE для Windows
1. Установите PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Соберите exe с иконкой:
   ```bash
   python build.py
   ```
   Готовый exe будет в папке `dist/` с именем `Directory analyzer.exe`.

## Как избежать ложных срабатываний антивирусов
- Не используйте обфускацию, packers, автозапуск, скрытые процессы
- Не добавляйте подозрительные импорты или сетевой код
- Собирайте на чистой системе с официальным Python и PyInstaller
- Подписывайте exe для распространения

## Лицензия
MIT License. См. файл [LICENSE](LICENSE).

---
GitHub: https://github.com/betrayalove/directory-structure-analyzer

---

# Directory Structure Analyzer

**A simple and user-friendly tool for visualizing and copying the structure of any directory. Supports Russian and English interface. Built with PyQt5.**

---

## Features
- Visual directory tree with clickable file links
- Copy file contents to clipboard
- Flexible filtering (hidden, system, dot, special, custom patterns)
- Language toggle (Russian/English)
- Customizable depth and indent
- No network access, no hidden processes

## Screenshot
*(Add your screenshot here)*

## Installation
1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Build Windows EXE
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable with icon:
   ```bash
   python build.py
   ```
   The EXE will be in the `dist/` folder as `Directory analyzer.exe`.

## Reducing Antivirus False Positives
- Do not use code obfuscation or packers
- Do not add auto-start or hidden features
- Do not use suspicious imports or network code
- Build on a clean system with official Python and PyInstaller
- Sign your EXE if possible (for distribution)

## License
MIT License. See [LICENSE](LICENSE).

---
GitHub: https://github.com/betrayalove/directory-structure-analyzer