import configparser

import discord
from yt_dlp import YoutubeDL


config = configparser.ConfigParser()
config.read('config/options.ini')

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def join_voice_channel(voice_channel):
    try:
        print('voice channelに接続します')
        voice_client = await voice_channel.connect()
        print('voice channelに接続しました')
        return voice_client
    except Exception as e:
        print(f'Error connecting to voice channel: {e}')
        return None


async def play_audio(voice_client, url, default_volume=config['Player']['DefaultVolume']):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }]
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            url2 = info_dict.get("url", None)
            source = await discord.FFmpegOpusAudio.from_probe(url2)
            volume_transformer = discord.PCMVolumeTransformer(source, volume=default_volume/100)
            voice_client.play(volume_transformer)
    except Exception as e:
        print(f'Error playing audio: {e}')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        url = message.content.split()[1]

        if message.author.voice is None or message.author.voice.channel is None:
            await message.channel.send("You need to connect to a voice channel first.")
            return

        voice_channel = message.author.voice.channel
        voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
        if voice_client and voice_client.is_playing():
            voice_client.stop()

        if not voice_client:
            voice_client = await join_voice_channel(voice_channel)
            if not voice_client:
                return

        await play_audio(voice_client, url)

client.run(config['Credentials']['Token'])
