import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

RADIO_STREAMS = {
    'rock': 'https://stream.pcradio.ru/Rock-hi',
    'rrd': 'https://stream1.radiord.ru:8000/live128.mp3',
}

class FFmpegHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters
        query = urlparse(self.path).query
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
           ['ffmpeg', '-re', "-fflags", "nobuffer", "-flags", "low_delay", '-i', stream_url, '-ab', '40k', '-ar', '32000', '-ac', '1', '-bufsize', '2048k', '-f', 'mp3', '-'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Stream the output of FFmpeg to the client
        try:
            while True:
                data = process.stdout.read(1024)  # Read in chunks
                if not data:
                    break
                self.wfile.write(data)
            process.stdout.close()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            process.terminate()

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
