import os
import subprocess
import time
from threading import Thread
from flask import Flask

STREAM_URL = os.getenv("YOUTUBE_STREAM_URL")
STREAM_KEY = os.getenv("YOUTUBE_STREAM_KEY")

app = Flask(__name__)

@app.route("/")
def health():
    return "Lofi stream alive ✅", 200

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def start_stream():
    while True:
        command = [
            "ffmpeg",
            "-re",
            "-stream_loop", "-1", "-t", "39600",  # 11 hours
            "-i", "music.mp3",
            "-loop", "1", "-framerate", "2", "-i", "stream.jpg",
            "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-f", "flv",
            f"{STREAM_URL}/{STREAM_KEY}"
        ]

        process = subprocess.Popen(command)
        process.wait()
        time.sleep(5)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    start_stream()
