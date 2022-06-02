import discord
from discord.ext import commands
import youtube_dl
import asyncio

bot = commands.Bot(command_prefix="!")
musics = {}
ytdl = youtube_dl.YoutubeDL()


@bot.event
async def on_ready():
    print("Ready")

# Fonction qui va prendre la musique sur youtube sans la télécharger
class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]


# Commande pour arrêter 
@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []


# Play après une pause
@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


# Pause
@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()

# Passer à la musique suivante qui se trouve dans la queue
@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()

# Fonction pour lire la piste audio de la vidéo Youtube
def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)

bot.run("OTc4MjI4ODUyNTc5MDAwMzMw.G6CN8h.3Paf6YhIAo-o5CxTMmeoxmeskDkJ3BIXLeQsqc")