FROM mcr.microsoft.com/devcontainers/python:0-3.9

# Install dependencies
RUN apt-get update && apt-get install \
ffmpeg \
libopus-dev \
libffi-dev \
libnacl-dev \
python-dev -y \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Install pip dependencies
RUN pip3 install --no-cache-dir yt-dlp pynacl discord
