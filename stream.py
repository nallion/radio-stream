import subprocess
from flask import Flask, Response
import yt_dlp

app = Flask(__name__)

# List of radio stations & YouTube Live links
RADIO_STATIONS = {
    "asianet_news": "https://vidcdn.vidgyor.com/live/asianetnews/index.m3u8",
    "24_news": "https://www.youtube.com/@24OnLive/live",
    "yaqeen_institute": "https://www.youtube.com/@YaqeenInstitute/live",
    "qsc_mukkam": "https://www.youtube.com/@quranhubmukkam/live",
    "shajahan_rahmani": "https://www.youtube.com/@ShajahanRahmani/live",
    "valiyudheen_faizy": "https://www.youtube.com/@ValiyudheenFaizy/live",

}

def get_youtube_audio_url(youtube_url):
    """ Extracts direct audio stream URL from YouTube Live """
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "extract_flat": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info["url"] if "url" in info else None

def generate_stream(url):
    """ Transcodes and serves audio using FFmpeg """
    process = subprocess.Popen(
        ["ffmpeg", "-i", url, "-b:a", "64k", "-f", "mp3", "-"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL  # Hide logs
    )
    return process.stdout

@app.route("/<station_name>")
def stream(station_name):
    """ Serve the requested station as a live stream """
    if station_name in RADIO_STATIONS:
        url = RADIO_STATIONS[station_name]

        # If it's a YouTube Live link, extract the audio stream
        if "youtube.com" in url or "youtu.be" in url:
            url = get_youtube_audio_url(url)
            if not url:
                return "Failed to get YouTube stream", 500

        return Response(generate_stream(url), mimetype="audio/mpeg")

    return "Station not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
