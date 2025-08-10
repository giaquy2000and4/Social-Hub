from flask import Flask, request, render_template, jsonify

from services.soundcloud_downloader import get_info_soundcloud, download_soundcloud
from services.tiktok_downloader import get_info_tiktok, download_tiktok
from services.youtube_downloader import get_info_youtube, download_youtube

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    media_info = None

    if request.method == 'POST':
        url = request.form.get('url')
        platform = request.form.get('platform')
        format_ = request.form.get('format')

        if platform == 'youtube':
            info = get_info_youtube(url)
        elif platform == 'tiktok':
            info = get_info_tiktok(url)
        elif platform == 'soundcloud':
            info = get_info_soundcloud(url)
        else:
            info = None

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

            # Thêm thông tin formats cho YouTube
            if platform == 'youtube':
                media_info.update({
                    'video_formats': info.get('video_formats', []),
                    'audio_formats': info.get('audio_formats', [])
                })

    return render_template('index.html', media_info=media_info)


@app.route('/download', methods=['POST'])
def download():
    # Nhận từ form POST
    data = request.form
    url = data.get('url')
    platform = data.get('platform')
    format_ = data.get('format')
    format_id = data.get('format_id')  # Thêm format_id để chọn chất lượng

    if platform == 'youtube':
        return download_youtube(url, format_, format_id)
    elif platform == 'tiktok':
        return download_tiktok(url, format_)
    elif platform == 'soundcloud':
        return download_soundcloud(url, format_)
    else:
        return jsonify({'error': 'Nền tảng không hợp lệ.'}), 400


if __name__ == "__main__":
    app.run(debug=True)