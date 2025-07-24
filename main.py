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
            "-stream_loop", "-1", "-i", "music.mp3",                 # Audio input loop
            # Video input loop (image), 30fps
            "-loop", "1", "-framerate", "30", "-i", "stream.jpg",
            # Ensure format
            "-filter_complex", "[1:v]format=yuv420p[v]",
            # Map video and audio
            "-map", "[v]", "-map", "0:a",
            "-s", "1280x720",                                        # Resolution
            "-r", "30",                                              # Force 30 fps
            "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",  # Encoding settings
            "-b:v", "3000k",                                         # Video bitrate
            # Keyframe every 2 sec (30 fps * 2 = 60)
            "-g", "60", "-keyint_min", "60",
            "-c:a", "aac", "-b:a", "192k",                           # Audio settings
            "-shortest",                                            # Ends with music
            "-f", "flv",                                             # FLV for YouTube RTMP
            f"{STREAM_URL}/{STREAM_KEY}"
        ]

        process = subprocess.Popen(command)
        process.wait()
        print("🔁 Stream ended/crashed. Restarting in 5s...")
        time.sleep(5)


if __name__ == "__main__":
    Thread(target=run_flask).start()
    start_stream()
