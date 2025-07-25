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
            "-loop", "1", "-framerate", "1", "-i", "image.jpg",  # 1 FPS
            "-filter_complex", "[1:v]format=yuv420p[v]",
            "-map", "[v]", "-map", "0:a",
            "-s", "640x360",
            "-r", "1",  # Output also 1 FPS to match
            "-c:v", "libx264", "-preset", "ultrafast", "-tune", "stillimage",
            "-b:v", "300k", "-maxrate", "500k", "-bufsize", "1000k",  # Very low bitrate
            # Keyframe every 2 frames (2 sec at 1 FPS)
            "-g", "2", "-keyint_min", "2",
            "-c:a", "aac", "-b:a", "96k",
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
