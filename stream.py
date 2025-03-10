from flask import Flask
from flask import stream_with_context, request, Response
import subprocess
import time

app = Flask(__name__)

@app.route("/")
def hello():
    def generate():
        startTime = time.time()
        buffer = []
        sentBurst = False

        ffmpeg_command = ["ffmpeg", "-i", "https://stream02.pcradio.ru/Rock-hi", "-acodec", "libmp3lame", "-ab", "40k", "-ac", "1", "-f", "mpeg", "pipe:stdout"]
        process = subprocess.Popen(ffmpeg_command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, bufsize = -1)

        while True:
            # Get some data from ffmpeg
            line = process.stdout.read(1024)

            # We buffer everything before outputting it
            buffer.append(line)

            # Minimum buffer time, 3 seconds
            if sentBurst is False and time.time() > startTime + 3 and len(buffer) > 0:
                sentBurst = True

                for i in range(0, len(buffer) - 2):
                    print "Send initial burst #", i
                    yield buffer.pop(0)

            elif time.time() > startTime + 3 and len(buffer) > 0:
                yield buffer.pop(0)

            process.poll()
            if isinstance(process.returncode, int):
                if process.returncode > 0:
                    print 'FFmpeg Error', p.returncode
                break

    return Response(stream_with_context(generate()), mimetype = "audio/mpeg")    

if __name__ == "__main__":
    app.run()
