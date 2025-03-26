import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs
import threading

# Define your available radio streams
RADIO_STREAMS = {
    'nashe': 'https://nashe1.hostingradio.ru:80/nashe-128.mp3',
    'dor': 'https://hls-01-dorognoe.emgsound.ru/15/112/playlist.m3u8',
    'rock': 'https://stream.pcradio.ru/Rock-hi',
    'rrd': 'https://stream1.radiord.ru:8000/live128.mp3',
    'angels': 'http://myradio24.org/angels',
    'freshrock': 'https://stream.freshrock.net/320.mp3', 
    'maximum': 'http://radioberezniki.ru:8000/berikimax',
    'glagol': 'https://a4.radioheart.ru:9007/nonstop',
    '32radio': 'https://online.guberniya.tv:8443/32radio_aac48',
    'nashe20': 'https://nashe1.hostingradio.ru:18000/nashe20-128.mp3',
    # Add more streams as needed
}

class FFmpegHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the request path
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/stats':
            # Handle the /stats request
            self.handle_stats()
        else:
            # Handle the radio stream requests
            self.handle_stream(parsed_path.query)

    def handle_stream(self, query):
        params = parse_qs(query)
        stream_key = params.get('stream', [None])[0]  # Get the 'stream' parameter

        if stream_key in RADIO_STREAMS:
            stream_url = RADIO_STREAMS[stream_key]
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Bad Request: Stream not found.')
            return

        self.send_response(200)
        self.send_header('Content-type', 'audio/mpeg')  # Change as necessary for your media type
        self.end_headers()

        # Start FFmpeg process to read from the selected stream
        process = subprocess.Popen(
            ['ffmpeg', '-i', stream_url, '-acodec', 'mp3', '-ab', '48k', '-ac', '1', '-f', 'mp3', '-'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Create a separate thread to handle stderr output
        def log_ffmpeg_output():
            for line in iter(process.stderr.readline, b''):
                print(line.decode('utf-8').strip())  # Print FFmpeg stderr output to console

        # Start the logging thread
        threading.Thread(target=log_ffmpeg_output, daemon=True).start()

        try:
            while True:
                data = process.stdout.read(1024)  # Read in chunks
                if not data:
                    break
                try:
                    self.wfile.write(data)
                except BrokenPipeError:
                    print("Client disconnected.")
                    break
                except Exception as e:
                    print(f"Error writing to client: {e}")
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            process.terminate()
            process.wait()  # Ensure the process has terminated

    def handle_stats(self):
        # Execute the 'ps -ax' command
        try:
            result = subprocess.run(['ps', '-ax'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(output.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Internal Server Error: {str(e)}'.encode('utf-8'))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

def run(server_class=ThreadedHTTPServer, handler_class=FFmpegHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
