import subprocess
import time
import json
from flask import Flask, Response

app = Flask(__name__)

# Store last played video ID to prevent repetition
last_played_video = None

def get_latest_youtube_video():
    """Fetches the latest video URL from MediaOne TV Live's YouTube channel."""
    global last_played_video
    channel_url = "https://www.youtube.com/@MediaoneTVLive/videos"
    
    try:
        command = ["yt-dlp", "--flat-playlist", "-J", channel_url]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            data = json.loads(result.stdout)
            if "entries" in data and len(data["entries"]) > 0:
                latest_video_id = data["entries"][0]["id"]
                if latest_video_id != last_played_video:
                    last_played_video = latest_video_id
                    return f"https://www.youtube.com/watch?v={latest_video_id}"
    except Exception as e:
        print(f"Error fetching latest video: {e}")
    
    return None


def get_youtube_audio_url(youtube_url):
    """Extracts direct audio stream URL from a YouTube video."""
    try:
        command = [
            "yt-dlp",
            "--cookies", "/mnt/data/cookies.txt",
            "--force-generic-extractor",
            "-f", "91",  # Audio format
            "-g", youtube_url
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Error extracting YouTube audio: {e}")

    return None


def generate_stream(url):
    """Streams audio using FFmpeg and auto-reconnects."""
    while True:
        process = subprocess.Popen(
            [
                "ffmpeg", "-reconnect", "1", "-reconnect_streamed", "1",
                "-reconnect_delay_max", "10", "-i", url, "-vn",
                "-b:a", "64k", "-buffer_size", "1024k", "-f", "mp3", "-"
            ],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=8192
        )

        print(f"Streaming from: {url}")

        try:
            for chunk in iter(lambda: process.stdout.read(8192), b""):
                yield chunk
        except GeneratorExit:
            process.kill()
            break
        except Exception as e:
            print(f"Stream error: {e}")

        print("FFmpeg stopped, restarting stream...")
        time.sleep(5)


@app.route("/latest_youtube")
def stream_latest_youtube():
    """Serve the latest YouTube video audio from MediaOne TV Live."""
    youtube_url = get_latest_youtube_video()
    
    if not youtube_url:
        return "Failed to get latest YouTube video", 500
    
    audio_url = get_youtube_audio_url(youtube_url)
    
    if not audio_url:
        return "Failed to get YouTube audio", 500
    
    return Response(generate_stream(audio_url), mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)