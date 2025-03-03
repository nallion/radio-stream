# Use a base image with Python and FFmpeg
FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y ffmpeg && \
    pip install flask yt-dlp

# Copy project files
WORKDIR /app
COPY stream.py .

# Expose the port Flask runs on
EXPOSE 8000

# Run the Flask app
CMD ["python", "stream.py"]
