# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg icecast2 && rm -rf /var/lib/apt/lists/*

# Expose port 8000
EXPOSE 8000
