# Discord MusicBot for Python

This is a simple Discord bot for playing music in voice channels. The bot can join a voice channel, play audio from YouTube videos, and manage the volume of the audio.

## Features

- Join a voice channel
- Play audio from YouTube videos
- Adjust the volume of the audio

## Installation

1. Install the required dependencies using pip:

```bash
$ pip install discord.py
$ pip install yt-dlp
```

2. Create a new file called config/options.ini and add the following content:

```csharp
[Credentials]
Token=YOUR_BOT_TOKEN

[Player]
DefaultVolume=YOUR_DESIRED_DEFAULT_VOLUME
```

Replace YOUR_BOT_TOKEN with your Discord bot token, and YOUR_DESIRED_DEFAULT_VOLUME with the desired default volume (0 to 100).

3. Run the bot script:

```bash
$ python main.py
```

## Usage

1. Connect to a voice channel.
2. Use the !play command followed by a YouTube video URL to start playing the audio in the voice channel.

```
!play https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Notes

This bot uses the discord.py library for interacting with Discord's API and the yt-dlp library for extracting audio from YouTube videos. It is important to keep these libraries up-to-date for the bot to function correctly.

Please keep in mind that this bot is a simple implementation and does not support advanced features like a queue system, skip, or pause functionality. Feel free to extend the bot according to your needs.
