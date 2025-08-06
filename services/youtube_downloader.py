import yt_dlp
import os

DOWNLOAD_FOLDER = 'downloads'

def get_info_youtube(url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception as e:
        print(f"[YouTube] Lỗi khi lấy info: {e}")
        return None

def download_youtube(url, format_):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    output_path = os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')

    if format_ == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
    else:  # video
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'quiet': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            if format_ == 'audio':
                file_path = file_path.rsplit('.', 1)[0] + '.mp3'
            return os.path.join(DOWNLOAD_FOLDER, os.path.basename(file_path))
    except Exception as e:
        print(f"[YouTube] Lỗi khi tải: {e}")
        return None
