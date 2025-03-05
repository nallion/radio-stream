import subprocess
from flask import Flask, Response
import yt_dlp

app = Flask(__name__)

# List of radio stations & YouTube Live links
RADIO_STATIONS = {
     "rubat_ataq": "http://stream.zeno.fm/5tpfc8d7xqruv",
    "shahul_radio": "https://stream-150.zeno.fm/cynbm5ngx38uv?zs=Ktca5StNRWm-sdIR7GloVg",
    "eram_fm": "http://icecast2.edisimo.com:8000/eramfm.mp3",
    "abc_islam": "http://s10.voscast.com:9276/stream",
    "al_sumood_fm": "http://us3.internet-radio.com/proxy/alsumoodfm2020?mp=/stream",
    "nur_ala_nur": "http://104.7.66.64:8011/",
    "ruqya_radio": "http://104.7.66.64:8004",
    "manjeri_fm": "https://air.pc.cdn.bitgravity.com/air/live/pbaudio101/chunklist.m3u8",
    "seiyun_radio": "http://s2.radio.co/s26c62011e/listen",
    "motivational_series": "http://104.7.66.64:8010",
    "deenagers_radio": "http://104.7.66.64:8003/",
    "real_fm": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio083/playlist.m3u8",
    "noor_al_eman": "http://edge.mixlr.com/channel/boaht",
    "radio_keralam": "http://ice31.securenetsystems.net/RADIOKERAL",
    "al_nour": "http://audiostreaming.itworkscdn.com:9066/",
    "muthnabi_radio": "http://cast4.my-control-panel.com/proxy/muthnabi/stream",
    "fm_gold": "https://airhlspush.pc.cdn.bitgravity.com/httppush/hispbaudio005/hispbaudio00564kbps.m3u8",
    "malayalam_90s": "https://stream-159.zeno.fm/gm3g9amzm0hvv?zs-x-7jq8ksTOav9ZhlYHi9xw",
    "aural_oldies": "https://stream-162.zeno.fm/tksfwb1mgzzuv?zs=SxeQj1-7R0alsZSWJie5eQ",
    "radio_malayalam": "https://radiomalayalamfm.com/radio/8000/radio.mp3",
    "swaranjali": "https://stream-161.zeno.fm/x7mve2vt01zuv?zs-D4nK05-7SSK2FZAsvumh2w",
    "sirat_al_mustaqim": "http://104.7.66.64:8091/stream",
    "air_calicut": "https://air.pc.cdn.bitgravity.com/air/live/pbaudio082/chunklist.m3u8",
    "sam_yemen": "https://edge.mixlr.com/channel/kijwr",
    "afaq": "https://edge.mixlr.com/channel/rumps",
    "al_jazeera": "http://live-his-audio-web-aja.getaj.net/VOICE-AJA/index.m3u8",
    "alfasi_radio": "https://qurango.net/radio/mishary_alafasi",
    "tafsir_quran": "https://radio.quranradiotafsir.com/9992/stream",
    "malayalam_1": "http://167.114.131.90:5412/stream",
    "urdu_islamic_lecture": "http://144.91.121.54:27001/channel_02.aac",
    "hob_nabi": "http://216.245.210.78:8098/stream",
    "sanaa_radio": "http://dc5.serverse.com/proxy/pbmhbvxs/stream",
    "radio_beat_malayalam": "http://live.exertion.in:8050/radio.mp3",
    "nonstop_hindi": "http://s5.voscast.com:8216/stream",
    "radio_digital_malayali": "https://radio.digitalmalayali.in/listen/stream/radio.mp3",
    "river_nile_radio": "http://104.7.66.64:8087",
    "quran_radio_cairo": "http://n02.radiojar.com/8s5u5tpdtwzuv?listening-from-radio-garden-1620219571863&rj-ttl=5&rj-tok=AAABivzcwaEAh735PZBqcATySw",
    "quran_radio_nablus": "http://www.quran-radio.org:8002/",
    "hajj_channel": "http://104.7.66.64:8005",
    "allahu_akbar_radio": "http://66.45.232.132.9996/",
    "omar_abdul_kafi_radio": "http://104.7.66.64:8007",
    "asianet_news": "https://vidcdn.vidgyor.com/asianet-origin/audioonly/chunks.m3u8",
    "yemen_talk": "http://stream.zeno.fm/7qv7c8eq7hhvv",
    "media_one": "https://www.youtube.com/watch?v=-8d8-c0yvyU",
    "safari_tv": "https://j78dp346yq5r-hls-live.5centscdn.com/safari/live.stream/chunks.m3u8",
    "victers_tv": "https://932y4x26ljv8-hls-live.5centscdn.com/victers/tv.stream/victers/tv1/chunks.m3u8",   
}

    
def get_youtube_audio_url(youtube_url):
    """Extracts direct audio stream URL from YouTube Live."""
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "cookies": "/mnt/data/cookies.txt",   # Path to cookies file
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
    process = subprocess.Popen(
        [
            "ffmpeg", "-reconnect", "1", "-reconnect_streamed", "1",
            "-reconnect_delay_max", "5", "-i", url, "-vn",
            "-b:a", "64k", "-f", "mp3", "-"
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
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
    app.run(host="0.0.0.0", port=8000, debug=True)


