document.addEventListener('DOMContentLoaded', function () {
    var downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.onclick = function () {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/download', true);
            xhr.responseType = 'blob';
            xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            var progressBar = document.getElementById('downloadProgress');
            var speedText = document.getElementById('speed');
            var lastLoaded = 0, lastTime = Date.now();

            xhr.onprogress = function (event) {
                if (event.lengthComputable) {
                    var percent = Math.round((event.loaded / event.total) * 100);
                    progressBar.style.width = percent + "%";
                    progressBar.textContent = percent + "%";

                    var now = Date.now();
                    var deltaBytes = event.loaded - lastLoaded;
                    var deltaTime = (now - lastTime) / 1000; // seconds
                    var speed = deltaBytes / deltaTime / 1024; // KB/s
                    speedText.textContent = "Tốc độ: " + speed.toFixed(2) + " KB/s";
                    lastLoaded = event.loaded;
                    lastTime = now;
                }
            };

            xhr.onload = function () {
                if (this.status === 200) {
                    var blob = this.response;
                    var url = window.URL.createObjectURL(blob);
                    var a = document.createElement('a');
                    a.href = url;
                    a.download = "song.mp3";
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    progressBar.style.width = "100%";
                    progressBar.textContent = "100%";
                    speedText.textContent = "Hoàn tất!";
                }
            };

            xhr.send(JSON.stringify({url: url}));
        };
    }
});
