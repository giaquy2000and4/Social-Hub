
# Audio Downloader Web Application

Ứng dụng web đơn giản được xây dựng bằng Flask, cho phép người dùng trích xuất và tải xuống âm thanh từ các nền tảng chia sẻ nội dung như SoundCloud, YouTube và nhiều dịch vụ khác được hỗ trợ bởi `yt-dlp`.

## Mô tả

Ứng dụng cung cấp giao diện người dùng thân thiện để:
- Nhập một liên kết từ dịch vụ chia sẻ nội dung (ví dụ: SoundCloud, YouTube).
- Phân tích và hiển thị thông tin về bài nhạc: tiêu đề, nghệ sĩ, ảnh bìa, thời lượng.
- Tải xuống phần âm thanh ở định dạng `.mp3` với chất lượng cao (192kbps).

Ứng dụng sử dụng `yt-dlp` để xử lý trích xuất dữ liệu và `FFmpeg` để chuyển đổi định dạng âm thanh.

## Yêu cầu hệ thống

- Python 3.7 hoặc mới hơn
- `pip` (Python package manager)
- `FFmpeg` đã được cài đặt và cấu hình vào biến môi trường `PATH`

## Cài đặt

### 1. Tạo môi trường ảo (khuyến nghị)
```bash
python -m venv venv
source venv/bin/activate       # Đối với Linux/macOS
venv\Scripts\activate          # Đối với Windows
````

### 2. Cài đặt các thư viện cần thiết

```bash
pip install flask yt-dlp
```

### 3. Cài đặt FFmpeg

* Tải về từ: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
* Thêm thư mục chứa `ffmpeg.exe` vào biến môi trường `PATH`.

## Cấu trúc dự án

```
├── app.py
├── templates/
│   └── index.html
├── downloads/
└── README.md
```

* `app.py`: Mã nguồn chính của ứng dụng Flask.
* `templates/index.html`: Giao diện người dùng.
* `downloads/`: Thư mục chứa các tệp âm thanh đã tải xuống.

## Cách sử dụng

1. Chạy ứng dụng:

   ```bash
   python app.py
   ```

2. Truy cập trình duyệt tại địa chỉ:

   ```
   http://127.0.0.1:5000
   ```

3. Sử dụng giao diện:

   * Nhập URL hợp lệ từ SoundCloud, YouTube hoặc nền tảng được hỗ trợ.
   * Xem trước thông tin bài hát.
   * Nhấn “Download” để tải tập tin MP3.

## Lưu ý

* Ứng dụng chỉ phục vụ mục đích học tập và nghiên cứu.
* Việc sử dụng ứng dụng với các nội dung có bản quyền phải tuân thủ quy định pháp luật và điều khoản dịch vụ của nền tảng tương ứng.
* Không sử dụng ứng dụng trong môi trường sản xuất khi đang bật chế độ `debug`.

```
