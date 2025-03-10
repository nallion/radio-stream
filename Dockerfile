FROM docker.io/library/debian:bullseye-slim


RUN apt update && apt upgrade -y && apt install -y sudo openssh-server && apt autoremove && apt clean && rm -rf /var/lib/apt/lists/*
    
EXPOSE 22
