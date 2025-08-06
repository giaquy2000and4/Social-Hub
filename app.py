from flask import Flask, request, send_file, render_template, jsonify
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
        song_info = {
            'title': info.get('title'),
            'artist': info.get('uploader') or info.get('artist', ''),
            'thumbnail': info.get('thumbnail', ''),
            'duration': info.get('duration', 0),
            'url': url
        }
        return render_template('index.html', song_info=song_info)
    return render_template('index.html', song_info=None)

@app.route('/download', methods=['POST'])
def download():
    url = request.json['url']
    output_path = os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')

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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        file_path = os.path.join(DOWNLOAD_FOLDER, os.path.basename(filename))

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
