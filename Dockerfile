# Use an official lightweight Python image
FROM python:3.9-slim

# Install dependencies
RUN sed -i 's/^Components: main$/& contrib non-free/' /etc/apt/sources.list.d/debian.sources
RUN apt-get update && apt-get install -y procps gcc make yasm libfdk-aac-dev libssl-dev wget && rm -rf /var/lib/apt/lists/*
RUN wget https://ffmpeg.org/releases/ffmpeg-4.4.5.tar.gz
RUN tar -xvf ffmpeg-4.4.5.tar.gz -C /usr/src
RUN cd /usr/src/ffmpeg-4.4.5/
RUN ./configure --enable-libfdk-aac --enable-openssl
RUN make
RUN make install

# Set the working directory
WORKDIR /app

COPY . .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["python", "restream.py"]
