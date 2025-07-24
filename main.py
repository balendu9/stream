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
            "-re",  # must come BEFORE the music input
            "-stream_loop", "-1", "-i", "music.mp3",  # Input 0: audio
            "-loop", "1", "-framerate", "1", "-i", "stream.jpg",  # Input 1: image
            "-filter_complex", "[1:v]format=yuv420p[v]",  # format fix
            # output video from image, audio from mp3
            "-map", "[v]", "-map", "0:a",
            "-s", "1280x720",
            "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
            "-b:v", "3000k", "-g", "8", "-keyint_min", "8",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",  # stop when the audio ends
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
