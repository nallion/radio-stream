import subprocess
import requests
from flask import Flask, Response

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
    "al_sumood_fm": "http://us3.internet-radio.com/proxy/alsumoodfm?mp=/stream",
    "nur_ala_nur": "http://104.7.66.64:8011/",
    "seiyun_radio": "http://s2.radio.co/s26c62011e/listen",
    "real_fm": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio083/playlist.m3u8",
    "noor_al_eman": "http://edge.mixlr.com/channel/boaht",
    "radio_keralam": "http://ice31.securenetsystems.net/RADIOKERAL",
    "al_nour": "http://audiostreaming.itworkscdn.com:9066/",
    "muthnabi_radio": "http://cast4.my-control-panel.com/proxy/muthnabi/stream",
    "fm_gold": "https://airhlspush.pc.cdn.bitgravity.com/httppush/hispbaudio005/hispbaudio00564kbps.m3u8",
    "malayalam_90s": "https://stream-159.zeno.fm/gm3g9amzm0hvv?zs-x-7jq8ks_TOav9ZhlYHi9xw",
    "aural_oldies": "https://stream-162.zeno.fm/tksfwb1mgzzuv?zs=SxeQj1-7R0alsZSWJie5eQ",
    "radio_malayalam": "https://radiomalayalamfm.com/radio/8000/radio.mp3",
    "swaranjali": "https://stream-161.zeno.fm/x7mve2vt01zuv?zs-D4nK05-7SSK2FZAsvumh2w",
    "sam_yemen": "https://edge.mixlr.com/channel/kijwr",
    "afaq": "https://edge.mixlr.com/channel/rumps",
    "al_jazeera": "http://live-his-audio-web-aja.getaj.net/VOICE-AJA/index.m3u8",
    "alfasi_radio": "https://qurango.net/radio/mishary_alafasi",
    "tafsir_quran": "https://radio.quranradiotafsir.com/9992/stream",
    "malayalam_1": "http://167.114.131.90:5412/stream",
    "sanaa_radio": "http://dc5.serverse.com/proxy/pbmhbvxs/stream",
    "radio_beat_malayalam": "http://live.exertion.in:8050/radio.mp3",
    "nonstop_hindi": "http://s5.voscast.com:8216/stream",
    "radio_digital_malayali": "https://radio.digitalmalayali.in/listen/stream/radio.mp3",
    "quran_radio_cairo": "http://n02.radiojar.com/8s5u5tpdtwzuv?listening-from-radio-garden-1620219571863&rj-ttl=5&rj-tok=AAABivzcwaEAh735PZBqcATySw",
    "quran_radio_nablus": "http://www.quran-radio.org:8002/",
    "allahu_akbar_radio": "http://66.45.232.132:9996/stream",
    "yemen_talk": "http://stream.zeno.fm/7qv7c8eq7hhvv",
    "hob_nabi": "http://216.245:210.78:8098/stream",
    "safari_tv": "https://j78dp346yq5r-hls-live.5centscdn.com/safari/live.stream/chunks.m3u8",
    "victers_tv": "https://932y4x26ljv8-hls-live.5centscdn.com/victers/tv.stream/victers/tv1/chunks.m3u8",
    "media_one": "https://www.youtube.com/@MediaoneTVLive/live",
}

# Change to a working Invidious instance
INVIDIOUS_INSTANCE = "https://vid.puffyan.us"

def get_invidious_audio_url(youtube_url):
    """Fetch direct audio URL from Invidious API."""
    video_id = youtube_url.split("v=")[-1] if "v=" in youtube_url else youtube_url.split("/")[-1]

    api_url = f"{INVIDIOUS_INSTANCE}/api/v1/videos/{video_id}"
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        # Extract best available audio URL
        for format in data.get("adaptiveFormats", []):
            if format.get("type") == "audio/mp4":
                return format["url"]

    except Exception as e:
        print(f"Error fetching from Invidious: {e}")
        return None

def generate_stream(url):
    """Transcodes and serves audio using FFmpeg."""
    process = subprocess.Popen(
        [
            "ffmpeg",
            "-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "5",
            "-i", url,
            "-vn", "-acodec", "libmp3lame", "-b:a", "64k",
            "-bufsize", "256k",
            "-fflags", "nobuffer",
            "-flush_packets", "1",
            "-f", "mp3", "-"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL  # Suppress FFmpeg logs
    )
    return process.stdout

@app.route("/<station_name>")
def stream(station_name):
    """Serve the requested station as a live stream."""
    url = RADIO_STATIONS.get(station_name)

    if not url:
        return "Station not found", 404

    if "youtube.com" in url or "youtu.be" in url:
        url = get_invidious_audio_url(url)
        if not url:
            return "Failed to get YouTube stream", 500

    return Response(generate_stream(url), mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
