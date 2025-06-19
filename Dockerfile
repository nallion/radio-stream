# Use an official debian image
FROM debian

# Install dependencies
RUN apt-get update && apt-get -y install ffmpeg && rm -rf /var/lib/apt/lists/*


# Set the working directory
WORKDIR /app

COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python3", "restream.py"]
