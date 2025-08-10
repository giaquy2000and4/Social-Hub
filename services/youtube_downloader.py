import yt_dlp
import tempfile
import os
import re
from flask import send_file
from io import BytesIO


def sanitize_filename(name):
    """Loại bỏ ký tự không hợp lệ khỏi tên file."""
    return re.sub(r'[\\/*?:"<>|]', "", name)


def format_filesize(bytes_size):
    """Chuyển đổi bytes thành định dạng dễ đọc."""
    if bytes_size is None:
        return "N/A"

    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def get_info_youtube(url):
    """Trả về thông tin media từ YouTube bao gồm các định dạng có sẵn."""
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

            # Lọc và sắp xếp các định dạng
            video_formats = []
            audio_formats = []

            for fmt in info.get('formats', []):
                format_note = fmt.get('format_note', '')
                ext = fmt.get('ext', '')
                filesize = fmt.get('filesize')

                # Định dạng video (có cả video và audio hoặc chỉ video)
                if fmt.get('vcodec') != 'none':
                    quality_label = fmt.get('height', 0)
                    if quality_label:
                        video_formats.append({
                            'format_id': fmt['format_id'],
                            'ext': ext,
                            'quality': f"{quality_label}p",
                            'note': format_note,
                            'filesize': format_filesize(filesize),
                            'fps': fmt.get('fps'),
                            'vcodec': fmt.get('vcodec', 'unknown'),
                            'acodec': fmt.get('acodec', 'none')
                        })

                # Định dạng audio (chỉ audio)
                elif fmt.get('acodec') != 'none':
                    abr = fmt.get('abr', 0)
                    if abr:
                        audio_formats.append({
                            'format_id': fmt['format_id'],
                            'ext': ext,
                            'quality': f"{int(abr)}kbps",
                            'note': format_note,
                            'filesize': format_filesize(filesize),
                            'acodec': fmt.get('acodec', 'unknown')
                        })

            # Sắp xếp theo chất lượng
            video_formats.sort(key=lambda x: x.get('fps', 0), reverse=True)
            video_formats.sort(key=lambda x: int(x['quality'].replace('p', '')), reverse=True)
            audio_formats.sort(key=lambda x: int(x['quality'].replace('kbps', '')), reverse=True)

            # Thêm thông tin formats vào info
            info['video_formats'] = video_formats
            info['audio_formats'] = audio_formats

            return info

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

            # Xác định format để tải
            if format_id:
                selected_format = format_id
            else:
                selected_format = 'bestaudio' if format_ == 'audio' else 'best'

            ydl_opts = {
                'format': selected_format,
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
                # Đối với video, nếu chọn format chỉ có video, cần merge với audio
                if format_id:
                    # Kiểm tra xem format có audio không
                    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        selected_fmt = next((f for f in info['formats'] if f['format_id'] == format_id), None)

                        if selected_fmt and selected_fmt.get('acodec') == 'none':
                            # Nếu không có audio, merge với audio tốt nhất
                            ydl_opts['format'] = f"{format_id}+bestaudio"

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