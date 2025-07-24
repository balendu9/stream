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
        print("🎧 Starting 11-hour stream")
        command = [
            "ffmpeg",
            "-stream_loop", "-1", "-i", "music.mp3",
            "-loop", "1", "-framerate", "2", "-i", "stream.jpg",
            "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
            "-b:v", "2500k",
            "-g", "8",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            "-f", "flv",
            f"{STREAM_URL}/{STREAM_KEY}"
        ]

        process = subprocess.Popen(command)
        process.wait()
        print("🔁 Stream ended/crashed. Restarting in 5s...")
        time.sleep(5)


if __name__ == "__main__":
    Thread(target=run_flask).start()
    start_stream()
