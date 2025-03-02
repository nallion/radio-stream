import os
import subprocess
import signal
import sys

# URL of the YouTube video
youtube_url = "https://www.youtube.com/watch?v=1wECsnGZcf/live"

# Use yt-dlp to extract audio and pipe it to FFmpeg
command = f'yt-dlp -f bestaudio -o - "{youtube_url}" | ffmpeg -i pipe:0 -acodec libmp3lame -b:a 128k -f mp3 pipe:1'

# Run the command
try:
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except Exception as e:
    print(f"Error starting subprocess: {e}")
    exit(1)

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print('Terminating process...')
    process.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Keep running
try:
    while True:
        output = process.stdout.read(1024)
        if not output:
            break
except KeyboardInterrupt:
    process.terminate()
