import subprocess
from flask import Flask, Response
import yt_dlp

app = Flask(__name__)

# List of radio stations & YouTube Live links
RADIO_STATIONS = {
    "asianet_news": "https://vidcdn.vidgyor.com/asianet-origin/audioonly/chunks.m3u8",
    "air_calicut": "https://air.pc.cdn.bitgravity.com/air/live/pbaudio082/chunklist.m3u8",
    "manjeri_fm": "https://air.pc.cdn.bitgravity.com/air/live/pbaudio101/chunklist.m3u8",
    "ruqya_radio": "http://104.7.66.64:8004",
    "motivational_series": "http://104.7.66.64:8010",
    "deenagers_radio": "http://104.7.66.64:8003/",
    "siratul_mustaqim": "http://104.7.66.64:8091/stream",
    "river_nile": "http://104.7.66.64:8087",
    "hajj_channel": "http://104.7.66.64:8005",
    "omar_kafi": "http://104.7.66.64:8007",
    "rubat_ataq": "http://stream.zeno.fm/5tpfc8d7xqruv",
    "shahul_radio": "https://stream-150.zeno.fm/cynbm5ngx38uv?zs=Ktca5StNRWm-sdIR7GloVg",
    "eram_fm": "http://icecast2.edisimo.com:8000/eramfm.mp3",
    "abc_islam": "http://s10.voscast.com:9276/stream",
    "al_sumood_fm": "http://us3.internet-radio.com/proxy/alsumoodfm?mp=/stream",
    "nur_ala_nur": "http://104.7.66.64:8011/",
    "seiyun_radio": "http://s2.radio.co/s26c62011e/listen",
    "real_fm": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio083/playlist.m3u8",
    "noor_al_eman": "http://edge.mixlr.com/channel/boaht",
    "radio_keralam": "http://ice31.securenetsystems.net/RADIOKERAL",
    "al_nour": "http://audiostreaming.itworkscdn.com:9066/",
    "muthnabi_radio": "http://cast4.my-control-panel.com/proxy/muthnabi/stream",
    "media_one": "https://www.youtube.com/@MediaoneTVLive/live",
    "safari_tv": "https://j78dp346yq5r-hls-live.5centscdn.com/safari/live.stream/chunks.m3u8",
    "victers_tv": "https://932y4x26ljv8-hls-live.5centscdn.com/victers/tv.stream/victers/tv1/chunks.m3u8",   
}

def get_youtube_audio_url(youtube_url):
    """Extracts direct audio stream URL from YouTube Live."""
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info.get("url")
    except Exception as e:
        print(f"Error extracting YouTube audio: {e}")
        return None

def generate_stream(url):
    """Transcodes and serves audio using FFmpeg with buffering fixes."""
    process = subprocess.Popen(
        [
            "ffmpeg",
            "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
            "-i", url,
            "-vn", "-acodec", "libmp3lame", "-b:a", "64k",
            "-bufsize", "256k",  # Increase buffer size to prevent skipping
            "-fflags", "nobuffer",  # Disable FFmpeg's default buffering
            "-flush_packets", "1",  # Ensure packets are sent immediately
            "-f", "mp3", "-"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL  # Suppress unnecessary FFmpeg logs
    )
    return process.stdout

@app.route("/<station_name>")
def stream(station_name):
    """Serve the requested station as a live stream."""
    url = RADIO_STATIONS.get(station_name)
    if not url:
        return "Station not found", 404

    if "youtube.com" in url or "youtu.be" in url:
        url = get_youtube_audio_url(url)
        if not url:
            return "Failed to get YouTube stream", 500

    return Response(generate_stream(url), mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True, debug=True)