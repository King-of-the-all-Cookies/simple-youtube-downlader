# Simple youtube downloader

[🇬🇧 English](#english-documentation) | [🇷🇺 Русский](#-русская-документация)

---

## 🇬🇧 English Documentation

# YouTube Downloader (Multilingual Console Tool)

📅 A console-based tool for downloading individual videos or playlists from YouTube in various formats and quality levels, with multilingual interface support.

### 📦 Features

* Download single videos or entire playlists.
* Format support:

  * **Audio**: `mp3`, `m4a`, `wav`, `flac`, `aac`, `opus`
  * **Video**: `mp4`, `mkv`, `webm`
* Choose quality (bitrate/resolution).
* Multilingual interface: English, Russian, Ukrainian, Japanese
* Automatic config file generation (`config.ini`)
* Colored console output using Colorama

### 🛠 Requirements

Install required libraries:

```bash
pip install yt-dlp colorama
```

Also install `ffmpeg` and specify the path in `config.ini`.

### ⚙ Configuration

On first run, a `config.ini` is generated:

```ini
[settings]
language = en              ; Available: en, ru, uk, ja
ffmpeg_path = ffmpeg/bin/ffmpeg.exe
```

Edit manually if needed.

### 🚀 Usage

Run via console:

```bash
python main.py
```

Step-by-step prompts:

1. Choose mode: single or playlist
2. Enter the URL
3. Confirm info
4. Select format (audio/video)
5. Choose quality
6. Wait for download

### 🗂 Example Output

**Video Info:**

```
Title: My Video
Duration: 00:03:45
Views: 123456
Likes: 7890
Dislikes: 123
```

**Playlist Info:**

```
No   Title                           Duration
1    First Song                     03:21
2    Second Track                   04:11
...
```

### ❗ Notes

* `ffmpeg` is required for audio conversion.
* Only public URLs are supported.

### 📁 License

This project is licensed under Apache 2.0.

---

## 🇷🇺 Русская документация

# YouTube Downloader (консольный загрузчик видео)

📅 Консольная утилита для скачивания одиночных видео или плейлистов с YouTube с поддержкой разных форматов и языков.

### 📦 Возможности

* Загрузка одного видео или плейлиста
* Поддержка форматов:

  * **Аудио**: `mp3`, `m4a`, `wav`, `flac`, `aac`, `opus`
  * **Видео**: `mp4`, `mkv`, `webm`
* Выбор качества (bitrate/разрешение)
* Многоязычный интерфейс: английский, русский, украинский, японский
* Сохранение настроек в `config.ini`
* Цветной вывод (с Colorama)

### 🛠 Зависимости

```bash
pip install yt-dlp colorama
```

Также нужен `ffmpeg`, путь к нему настраивается в `config.ini`.

### ⚙ Конфигурация

При первом запуске создается `config.ini`:

```ini
[settings]
language = ru              ; en, ru, uk, ja
ffmpeg_path = ffmpeg/bin/ffmpeg.exe
```

### 🚀 Использование

Запуск:

```bash
python main.py
```

Ваши действия:

1. Выбор режима: один ролик или плейлист
2. Ввод URL
3. Подтверждение информации
4. Выбор формата
5. Выбор качества
6. Ожидание загрузки

### 🗂 Пример вывода

**Видео:**

```
Title: Мое видео
Duration: 00:03:45
Views: 123456
Likes: 7890
Dislikes: 123
```

**Плейлист:**

```
No   Title                         Duration
1    Первый трек              03:21
2    Второй трек             04:11
...
```

### ❗ Заметки

* `ffmpeg` нужен для конвертации аудио
* Поддерживаются только открытые URL

### 📁 Лицензия

Проект распространяется по лицензии Apache 2.0.
