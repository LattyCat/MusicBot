import configparser

import discord
from yt_dlp import YoutubeDL


config = configparser.ConfigParser()
config.read('config/options.ini')

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!play'):
        url = message.content.split()[1]
        voice_channel = message.author.voice.channel
        if not voice_channel:
            # メッセージを送信したユーザが音声チャンネルに接続していない場合はエラーを送信する
            await message.channel.send(
                "You need to connect to a voice channel first.")
            return
        else:
            # Check if the bot is already connected to a voice channel
            voice_client = discord.utils.get(client.voice_clients, guild=message.guild)
            if voice_client and voice_client.is_playing():
                # Stop the current audio playback
                voice_client.stop()

            if not voice_client:
                # ボイスチャンネルに参加
                try:
                    print('voice channelに接続します')
                    voice_client = await voice_channel.connect()
                    print('voice channelに接続しました')
                except Exception as e:
                    print(f'Error connecting to voice channel: {e}')
                    return

            # Youtubeから音声をダウンロードして再生
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
                    voice_client.play(source)
            except Exception as e:
                print(f'Error playing audio: {e}')
                return

client.run(config['Credentials']['Token'])
