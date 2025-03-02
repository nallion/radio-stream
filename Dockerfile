# Use Python base image
# Use Python base image
FROM python:3.9

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Copy files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start script
CMD ["python3", "script.py"]
