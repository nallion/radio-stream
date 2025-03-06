from flask import Flask, Response
import yt_dlp
import subprocess

app = Flask(__name__)

# Use the proper channel URL format (replace with the actual ID)
CHANNEL_URL = "https://www.youtube.com/c/24onLive"

def get_latest_video_url():
    """Fetch the latest video URL from the given YouTube channel."""
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "force_generic_extractor": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(CHANNEL_URL, download=False)
        if "_entries" in info and len(info["_entries"]) > 0:
            return info["_entries"][0]["url"]  # Latest video URL
    return None

def get_latest_audio_url():
    """Get the direct audio stream URL of the latest video."""
    video_url = get_latest_video_url()
    if not video_url:
        return None

    ydl_opts = {
        "quiet": True,
        "format": "bestaudio",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info.get("url") if info else None

@app.route("/play")
def play_audio():
    """Stream the latest YouTube video's audio using FFmpeg."""
    audio_url = get_latest_audio_url()
    if not audio_url:
        return "No audio found", 404

    # Stream using FFmpeg
    command = [
        "ffmpeg", "-i", audio_url, "-vn", "-acodec", "libmp3lame", "-b:a", "128k",
        "-f", "mp3", "pipe:1"
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    return Response(process.stdout, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)