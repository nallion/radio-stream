# Use a base image with Python and FFmpeg
FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y ffmpeg && \
    pip install --no-cache-dir flask yt-dlp

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Expose the correct port
EXPOSE 3000

# Run the Flask app
CMD ["python", "stream.py"]
