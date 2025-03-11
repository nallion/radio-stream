# Use an official lightweight Python image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python", "restream.py"]
