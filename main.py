import asyncio
import configparser
import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

config = configparser.ConfigParser()
config.read('config/options.ini')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
volume_transformer = None


async def join_voice_channel(voice_channel):
    print('voice channelに接続します')
    voice_client = await voice_channel.connect()
    print('voice channelに接続しました')
    return voice_client


async def play_audio(voice_client, url, default_volume=int(
        config['player']['default_volume'])):
    global volume_transformer
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
        voice_client.play(volume_transformer, after=lambda e:
                          asyncio.run_coroutine_threadsafe(
                            disconnect_after_timeout(voice_client), bot.loop))
    asyncio.create_task(disconnect_after_timeout(voice_client))


async def user_in_voice_channel(ctx):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("音声チャンネルに接続してからコマンドを実行してください")
        return False
    return True


async def disconnect_after_timeout(voice_client, timeout=180):
    await asyncio.sleep(timeout)
    if not voice_client.is_playing():
        await voice_client.disconnect()


def change_volume(new_volume):
    global volume_transformer
    if volume_transformer is not None:
        volume_transformer.volume = new_volume / 100


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def play(ctx, url):
    if not await user_in_voice_channel(ctx):
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
    if not await user_in_voice_channel(ctx):
        return

    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        asyncio.create_task(disconnect_after_timeout(voice_client))


@bot.command()
async def volume(ctx, new_volume: int):
    if new_volume < 0 or new_volume > 100:
        await ctx.send("ボリュームは0から100の範囲で指定してください。")
        return

    change_volume(new_volume)
    await ctx.send(f"ボリュームを{new_volume}%に設定しました。")

bot.run(config['credentials']['token'])
