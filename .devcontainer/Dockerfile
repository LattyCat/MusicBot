FROM mcr.microsoft.com/devcontainers/python:0-3.11

# Install dependencies
RUN apt-get update && apt-get install \
ffmpeg \
libffi-dev \
libnacl-dev \
python3-dev -y \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Install pip dependencies
RUN pip3 install --no-cache-dir youtube_dl pynacl 'discord.py==1.7.3'
