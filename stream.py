import subprocess
from flask import Flask, Response
import yt_dlp

app = Flask(__name__)

RADIO_STATIONS = {
    "asianet_news": "https://vidcdn.vidgyor.com/asianet-origin/audioonly/chunks.m3u8",
    "suprabhatam_online": "https://www.youtube.com/channel/UCsPsEKy0BeYpuLW5IGoTDrw/live",
    "media_one": "https://www.youtube.com/@MediaoneTVLive/live",
    "24_news": "https://www.youtube.com/@24OnLive/live",
    "shajahan_rahmani": "https://www.youtube.com/@ShajahanRahmaniOfficial/live",
    "qsc_mukkam": "https://www.youtube.com/c/quranstudycentremukkam/live",
    "valiyudheen_faizy": "https://www.youtube.com/@voiceofvaliyudheenfaizy600/live",
    "skicr_tv": "https://www.youtube.com/@SKICRTV/live",
    "yaqeen_institute": "https://www.youtube.com/@yaqeeninstituteofficial/live",
    "bayyinah_tv": "https://www.youtube.com/@bayyinah/live",
       
}

def get_youtube_audio_url(youtube_url):
    """Extracts direct audio stream URL from YouTube Live."""
    try:
        ydl_opts = {
            "format": "bestaudio",
            "quiet": True,
            "noplaylist": True,
            "geo_bypass": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            if "url" in info:
                return info["url"]
    except Exception as e:
        print(f"Error extracting YouTube audio: {e}")
    return None

def generate_stream(url):
    """Transcodes and serves audio using FFmpeg."""
    try:
        process = subprocess.Popen(
            ["ffmpeg", "-re", "-i", url, "-vn", "-b:a", "64k", "-f", "mp3", "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        while True:
            chunk = process.stdout.read(4096)
            if not chunk:
                break
            yield chunk
    except Exception as e:
        print(f"FFmpeg error: {e}")

@app.route("/<station_name>")
def stream(station_name):
    """Serve the requested station as a live stream."""
    if station_name in RADIO_STATIONS:
        url = RADIO_STATIONS[station_name]
        if "youtube.com" in url or "youtu.be" in url:
            url = get_youtube_audio_url(url)
            if not url:
                return "Failed to get YouTube stream", 500
        return Response(generate_stream(url), mimetype="audio/mpeg")
    return "Station not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
