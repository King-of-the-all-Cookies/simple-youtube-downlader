import os
import sys
import configparser
import datetime
from yt_dlp import YoutubeDL
from colorama import init, Fore
import tkinter as tk
from tkinter import filedialog

init(autoreset=True)
CONFIG_PATH = 'config.ini'

DEFAULT_MESSAGES = {
    'en': {
        'mode_prompt': "Choose download mode:\n1) Single video\n2) Playlist",
        'enter_url': "Enter the URL:",
        'video_info': "Video info:",
        'playlist_info': "Playlist info (Index | Title | Duration):",
        'confirm_prompt': "Is this correct? (y/n)",
        'format_prompt': "Choose output format by number:",
        'quality_prompt_audio': "Choose audio quality by number:",
        'quality_prompt_video': "Choose video resolution by number:",
        'error': "Invalid choice, returning to main menu.",
        'url_error': "Failed to retrieve info. Please check the URL and try again.",
        'download_error': "Error occurred during download. Please try again.",
        'restart_prompt': "Return to main menu? (y/n)",
        'goodbye': "Goodbye!"
    },
    'ru': {
        'mode_prompt': "Выберите режим загрузки:\n1) Одно видео\n2) Плейлист",
        'enter_url': "Введите URL:",
        'video_info': "Информация о видео:",
        'playlist_info': "Информация о плейлисте (№ | Название | Длительность):",
        'confirm_prompt': "Все верно? (y/n)",
        'format_prompt': "Выберите формат по номеру:",
        'quality_prompt_audio': "Выберите качество аудио по номеру:",
        'quality_prompt_video': "Выберите разрешение видео по номеру:",
        'error': "Неверный выбор, возвращаемся в главное меню.",
        'url_error': "Не удалось получить информацию. Проверьте URL и попробуйте снова.",
        'download_error': "Ошибка при загрузке. Пожалуйста, попробуйте снова.",
        'restart_prompt': "Вернуться в главное меню? (y/n)",
        'goodbye': "До свидания!"
    },
    'uk': {
        'mode_prompt': "Оберіть режим завантаження:\n1) Одне відео\n2) Плейлист",
        'enter_url': "Введіть URL:",
        'video_info': "Інформація про відео:",
        'playlist_info': "Інформація про плейлист (№ | Назва | Тривалість):",
        'confirm_prompt': "Все вірно? (y/n)",
        'format_prompt': "Виберіть формат за номером:",
        'quality_prompt_audio': "Виберіть якість аудіо за номером:",
        'quality_prompt_video': "Виберіть роздільну здатність відео за номером:",
        'error': "Неправильний вибір, повертаємось у головне меню.",
        'url_error': "Не вдалося отримати інформацію. Перевірте URL і спробуйте знову.",
        'download_error': "Помилка під час завантаження. Будь ласка, спробуйте ще раз.",
        'restart_prompt': "Повернутися до головного меню? (y/n)",
        'goodbye': "До побачення!"
    },
    'ja': {
        'mode_prompt': "ダウンロードモードを選択してください:\n1) 単一動画\n2) プレイリスト",
        'enter_url': "URLを入力してください:",
        'video_info': "動画情報:",
        'playlist_info': "プレイリスト情報 (番号 | タイトル | 長さ):",
        'confirm_prompt': "これでよろしいですか？ (y/n)",
        'format_prompt': "番号で保存形式を選択してください:",
        'quality_prompt_audio': "番号でオーディオ品質を選択してください:",
        'quality_prompt_video': "番号でビデオ解像度を選択してください:",
        'error': "無効な選択です。メインメニューに戻ります。",
        'url_error': "情報の取得に失敗しました。URLを確認して再度お試しください。",
        'download_error': "ダウンロード中にエラーが発生しました。もう一度お試しください。",
        'restart_prompt': "メインメニューに戻りますか？ (y/n)",
        'goodbye': "さようなら！"
    }
}

AUDIO_FORMATS = ['mp3', 'm4a', 'wav', 'flac', 'aac', 'opus']
VIDEO_FORMATS = ['mp4', 'mkv', 'webm']
OUTPUT_FORMATS = AUDIO_FORMATS + VIDEO_FORMATS

AUDIO_QUALITY = ['64', '96', '128', '192', '256', '320']
VIDEO_QUALITY = ['144', '240', '360', '480', '720', '1080', '1440', '2160', '4320']


def ensure_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write('; Available languages: en, ru, uk, ja\n')
            f.write('[settings]\n')
            f.write('language = en\n')
            f.write('ffmpeg_path = ffmpeg/bin/ffmpeg.exe\n')


def load_settings():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH, encoding='utf-8')
    lang = config.get('settings', 'language', fallback='en')
    ffmpeg = config.get('settings', 'ffmpeg_path', fallback='ffmpeg')
    if lang not in DEFAULT_MESSAGES:
        lang = 'en'
    return lang, ffmpeg


def format_duration(seconds):
    return str(datetime.timedelta(seconds=seconds)) if seconds else 'N/A'


def print_video_info(info):
    print(Fore.CYAN + f"Title: {info.get('title')}")
    print(Fore.CYAN + f"Duration: {format_duration(info.get('duration'))}")
    print(Fore.YELLOW + f"Views: {info.get('view_count')}")
    print(Fore.YELLOW + f"Likes: {info.get('like_count')}")
    print(Fore.YELLOW + f"Dislikes: {info.get('dislike_count')}")


def print_playlist_table(info):
    print(Fore.MAGENTA + f"{'No':<4} {'Title':<50} {'Duration':<10}")
    for i, entry in enumerate(info.get('entries', []), 1):
        title = entry.get('title', 'N/A')[:50]
        dur = format_duration(entry.get('duration'))
        print(Fore.WHITE + f"{i:<4} {title:<50} {dur:<10}")


def get_info(url, opts):
    try:
        with YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception:
        return None


def download(url, opts):
    try:
        with YoutubeDL(opts) as ydl:
            ydl.download([url])
        return True
    except Exception:
        return False


def ask_download_dir():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select download folder")
    if not directory:
        directory = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(directory, exist_ok=True)
    return directory


def set_metadata_hook(info):
    # Set metadata for audio files
    if info.get('filepath', '').endswith(tuple(AUDIO_FORMATS)):
        # Basic metadata
        metadata = {
            'title': info.get('title', ''),
            'artist': info.get('uploader', ''),
        }
        
        # Track number for playlists
        if info.get('playlist_index') is not None:
            metadata['track'] = str(info['playlist_index'])
        
        # Add metadata to FFmpeg arguments
        args = []
        for key, value in metadata.items():
            if value:
                args.extend(['-metadata', f'{key}={value}'])
        
        return args
    return []


def main():
    ensure_config()
    lang, ffmpeg_path = load_settings()
    msgs = DEFAULT_MESSAGES[lang]
    os.environ['FFMPEG_LOCATION'] = ffmpeg_path

    while True:
        print(Fore.GREEN + msgs['mode_prompt'])
        choice = input('> ').strip()
        if choice not in ('1', '2'):
            print(Fore.RED + msgs['error'])
            continue

        url = input(Fore.BLUE + msgs['enter_url'] + ' ').strip()
        info = get_info(url, {'format': 'bestaudio/best', 'ignoreerrors': True})
        if not info:
            print(Fore.RED + msgs['url_error'])
            continue

        if choice == '1':
            print(Fore.GREEN + msgs['video_info'])
            print_video_info(info)
        else:
            print(Fore.GREEN + msgs['playlist_info'])
            print_playlist_table(info)

        if input(Fore.GREEN + msgs['confirm_prompt'] + ' ').lower() != 'y':
            continue

        print(Fore.GREEN + msgs['format_prompt'])
        for idx, fmt in enumerate(OUTPUT_FORMATS, 1):
            print(Fore.CYAN + f"[{idx}] - {fmt}")
        fc = input('> ').strip()
        if not fc.isdigit() or not (1 <= int(fc) <= len(OUTPUT_FORMATS)):
            print(Fore.RED + msgs['error'])
            continue
        out_fmt = OUTPUT_FORMATS[int(fc) - 1]

        if out_fmt in AUDIO_FORMATS:
            print(Fore.GREEN + msgs['quality_prompt_audio'])
            for idx, q in enumerate(AUDIO_QUALITY, 1):
                print(Fore.CYAN + f"[{idx}] - {q} kbps")
            qc = input('> ').strip()
            if not qc.isdigit() or not (1 <= int(qc) <= len(AUDIO_QUALITY)):
                print(Fore.RED + msgs['error'])
                continue
            quality = AUDIO_QUALITY[int(qc) - 1]
            download_dir = ask_download_dir()
            
            ydl_opts = {
                'format': f'bestaudio[abr<={quality}]/bestaudio/best',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': out_fmt,
                        'preferredquality': quality,
                    },
                    {
                        'key': 'FFmpegMetadata',
                        'add_metadata': True,
                    },
                    {
                        'key': 'EmbedThumbnail',
                        'already_have_thumbnail': False,
                    }
                ],
                'writethumbnail': True,
                'outtmpl': f"{download_dir}/%(title)s.%(ext)s",
                'ignoreerrors': True,
                'postprocessor_hooks': [set_metadata_hook],
            }
        else:
            print(Fore.GREEN + msgs['quality_prompt_video'])
            for idx, q in enumerate(VIDEO_QUALITY, 1):
                print(Fore.CYAN + f"[{idx}] - {q}p")
            qc = input('> ').strip()
            if not qc.isdigit() or not (1 <= int(qc) <= len(VIDEO_QUALITY)):
                print(Fore.RED + msgs['error'])
                continue
            resolution = VIDEO_QUALITY[int(qc) - 1]
            download_dir = ask_download_dir()
            ydl_opts = {
                'format': f'bestvideo[height<={resolution}]+bestaudio/best',
                'merge_output_format': out_fmt,
                'outtmpl': f"{download_dir}/%(title)s.%(ext)s",
                'ignoreerrors': True
            }

        if not download(url, ydl_opts):
            print(Fore.RED + msgs['download_error'])
            continue

        if input(Fore.GREEN + msgs['restart_prompt'] + ' ').lower() != 'y':
            print(Fore.YELLOW + msgs['goodbye'])
            sys.exit(0)


if __name__ == '__main__':
    main()
