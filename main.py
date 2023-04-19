import configparser
import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

config = configparser.ConfigParser()
config.read('config/options.ini')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


async def join_voice_channel(voice_channel):
    print('voice channelに接続します')
    voice_client = await voice_channel.connect()
    print('voice channelに接続しました')
    return voice_client


async def play_audio(voice_client, url, default_volume):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
            'preferredquality': '192',
        }]
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        url2 = info_dict.get("url", None)
        source = discord.FFmpegPCMAudio(url2, options="-acodec pcm_s16le")
        volume_transformer = discord.PCMVolumeTransformer(
            source, volume=default_volume / 100)
        voice_client.play(volume_transformer)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def play(ctx, url):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("音声チャンネルに接続してからコマンドを実行してください")
        return

    voice_channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()

    if not voice_client:
        try:
            voice_client = await join_voice_channel(voice_channel)
        except Exception as e:
            print(f'Error connecting to voice channel: {e}')
            return

    try:
        default_volume = int(config['player']['default_volume'])
        await play_audio(voice_client, url, default_volume)
    except Exception as e:
        print(f'Error playing audio: {e}')


@bot.command()
async def stop(ctx):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("音声チャンネルに接続してからコマンドを実行してください")
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()

bot.run(config['credentials']['token'])
