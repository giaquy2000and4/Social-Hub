from flask import Flask, request, render_template, send_file, jsonify
import os

# Import các service riêng cho từng nền tảng
from services.youtube_downloader import get_info_youtube, download_youtube
from services.tiktok_downloader import get_info_tiktok, download_tiktok
from services.soundcloud_downloader import get_info_soundcloud, download_soundcloud

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    media_info = None

    if request.method == 'POST':
        url = request.form.get('url')
        platform = request.form.get('platform')
        format_ = request.form.get('format')

        # Gọi service tùy theo nền tảng
        if platform == 'youtube':
            info = get_info_youtube(url)
        elif platform == 'tiktok':
            info = get_info_tiktok(url)
        elif platform == 'soundcloud':
            info = get_info_soundcloud(url)
        else:
            info = None

        # Chuẩn hóa info để render ra giao diện
        if info:
            media_info = {
                'title': info.get('title', 'Không có tiêu đề'),
                'uploader': info.get('uploader', 'Không rõ'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'url': url,
                'platform': platform,
                'format': format_
            }

    return render_template('index.html', media_info=media_info)


@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    platform = data.get('platform')
    format_ = data.get('format')

    file_path = None

    if platform == 'youtube':
        file_path = download_youtube(url, format_)
    elif platform == 'tiktok':
        file_path = download_tiktok(url, format_)
    elif platform == 'soundcloud':
        file_path = download_soundcloud(url, format_)

    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'Tải không thành công.'}), 400


if __name__ == "__main__":
    app.run(debug=True)
