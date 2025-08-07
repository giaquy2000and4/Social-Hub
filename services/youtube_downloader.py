import yt_dlp
import tempfile
import os
import re
from flask import send_file
from io import BytesIO

def sanitize_filename(name):
    """Loại bỏ ký tự không hợp lệ khỏi tên file."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def get_info_youtube(url):
    """Trả về thông tin media từ YouTube để hiển thị lên giao diện và chọn định dạng."""
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception as e:
        print(f"[YouTube] Lỗi khi lấy thông tin: {e}")
        return None

def download_youtube(url, format_, format_id=None):
    """
    Tải file từ YouTube với định dạng và chất lượng được chỉ định.
    - url: liên kết video
    - format_: 'audio' hoặc 'video'
    - format_id: định danh chất lượng được chọn từ dropdown
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, '%(title)s.%(ext)s')

            ydl_opts = {
                'format': format_id if format_id else ('bestaudio' if format_ == 'audio' else 'best'),
                'outtmpl': output_path,
                'ffmpeg_location': 'C:\\ProgramData\\chocolatey\\bin',  # <-- thay bằng đúng đường dẫn máy bạn
                'quiet': True
            }

            # Nếu là audio, cần hậu xử lý để chuyển sang MP3
            if format_ == 'audio':
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                ext = 'mp3'
                mimetype = 'audio/mpeg'
            else:
                ext = 'mp4'
                mimetype = 'video/mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if format_ == 'audio':
                    filename = os.path.splitext(filename)[0] + '.mp3'

            # Đọc file đã tải vào RAM
            with open(filename, 'rb') as f:
                file_data = BytesIO(f.read())
            file_data.seek(0)

            title = sanitize_filename(info.get('title', 'media'))
            final_name = f"{title}.{ext}"

            return send_file(
                file_data,
                as_attachment=True,
                download_name=final_name,
                mimetype=mimetype
            )

    except Exception as e:
        print(f"[YouTube] Lỗi khi tải file: {e}")
        return None
