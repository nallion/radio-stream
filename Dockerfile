FROM debian:stable-slim
# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg icecast2 && rm -rf /var/lib/apt/lists/*
RUN /etc/init.d/icecast2 start

# Expose port 8000
EXPOSE 8000
