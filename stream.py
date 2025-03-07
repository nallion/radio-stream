import subprocess
import time
from flask import Flask, Response

app = Flask(__name__)

# 📡 List of YouTube Live Streams
YOUTUBE_STREAMS = {
    "media_one": "https://www.youtube.com/@MediaoneTVLive/live",
    "shajahan_rahmani": "https://www.youtube.com/@ShajahanRahmaniOfficial/live",
    "qsc_mukkam": "https://www.youtube.com/c/quranstudycentremukkam/live",
    "valiyudheen_faizy": "https://www.youtube.com/@voiceofvaliyudheenfaizy600/live",
    "skicr_tv": "https://www.youtube.com/@SKICRTV/live",
    "yaqeen_institute": "https://www.youtube.com/@yaqeeninstituteofficial/live",
    "bayyinah_tv": "https://www.youtube.com/@bayyinah/live",
}

# 🎵 Extract direct audio stream URL using yt-dlp
def get_audio_url(youtube_url):
    command = [
        "yt-dlp",
        "--cookies", "/mnt/data/cookies.txt",
        "--force-generic-extractor",
        "-f", "140",  # Audio format
        "-g", youtube_url
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip() if result.stdout else None
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error fetching audio URL: {e}")
        return None

# 🔄 Stream YouTube audio via FFmpeg
def generate_stream(youtube_url):
    process = None
    while True:
        if process:
            process.kill()

        stream_url = get_audio_url(youtube_url)
        if not stream_url:
            print("⚠️ Failed to fetch stream URL")
            return
        
        process = subprocess.Popen(
            ["ffmpeg", "-reconnect", "1", "-reconnect_streamed", "1",
             "-reconnect_delay_max", "10", "-i", stream_url,
             "-vn", "-b:a", "64k", "-buffer_size", "1024k", "-f", "mp3", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=8192
        )

        print(f"🎵 Streaming from: {youtube_url}")

        try:
            for chunk in iter(lambda: process.stdout.read(8192), b""):
                yield chunk
        except GeneratorExit:
            process.kill()
            break
        except Exception as e:
            print(f"⚠️ Stream error: {e}")

        print("🔄 FFmpeg stopped, restarting stream...")
        time.sleep(5)

# 🌍 API to play YouTube live audio
@app.route("/play/<station_name>")
def stream(station_name):
    youtube_url = YOUTUBE_STREAMS.get(station_name)
    if not youtube_url:
        return "⚠️ Station not found", 404
    
    return Response(generate_stream(youtube_url), mimetype="audio/mpeg")

# 🚀 Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)