import os
import subprocess
import signal
import sys

# URL of the YouTube video
youtube_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"  # Replace with your YouTube URL

# Stream audio to another device (e.g., Icecast server)
# Replace icecast_url, username, and password with your streaming server details
icecast_url = "http://your-icecast-server:8000/stream"
username = "source"
password = "your_password"

# Command to stream audio using yt-dlp and ffmpeg
command = (
    f'yt-dlp -f bestaudio -o - "{youtube_url}" | '
    f'ffmpeg -i pipe:0 -acodec libmp3lame -b:a 128k -f mp3 -content_type audio/mpeg '
    f'icecast://{username}:{password}@{icecast_url}'
)

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
