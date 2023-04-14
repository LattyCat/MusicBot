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
        if message.author.voice is None:
            # メッセージを送信したユーザが音声チャンネルに接続していない場合はエラーを送信する
            await message.channel.send(
                "You need to connect to a voice channel first."
                )
            return
        else:
            # ボイスチャンネルに参加
            print('voice channel join')
            voice_client = await voice_channel.connect()
            print('voice channelに接続しました')

            # Youtubeから音声をダウンロードして再生
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

client.run(config['Credentials']['Token'])
