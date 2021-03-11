import asyncio
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get

ytdl_format_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'restrictfilenames': True,
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'audioformat': 'mp3',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1  -reconnect_delay_max 5',    
                  'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))

        # take first item from a playlist
        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                   data=data)


class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client

    def check_queue(self, id):
        if self.queue[id]:
            player = self.queue[id].pop(0)
            self.players[id] = player
            player.start()

    @commands.command()
    async def join(self, ctx):
        """join channel"""
        if not ctx.voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            # print(f"Oni has connected to {channel}")

    @commands.command(aliases=["stop"])
    async def leave(self, ctx):
        """leave channel"""
        # channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        # await self.client.change_presence(activity=discord.Activity(type=0, name=f"ready"))
        await voice.disconnect()
        # print(f"The bot has left {channel}")

    @commands.command(aliases=["stream", "yt"])
    async def play(self, ctx, *, url):
        """stream song from youtube"""
        await self.join(ctx)
        async with ctx.typing():
            voice = await YTDLSource.from_url(url,
                                              loop=self.client.loop,
                                              stream=True)
            ctx.voice_client.play(voice,
                                  after=lambda e: print('Player error: %s' % e)
                                  if e else None)

        await ctx.send('> now playing: {}'.format(voice.title))
        # await self.client.change_presence(activity=discord.Activity(type=0, name="{}".format(voice.title)))

    @commands.command(aliases=["pau"])
    async def pause(self, ctx):
        """pause audio"""
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            # print("music paused")
            voice.pause()
        # else:
        #     print("music not playing")

    @commands.command(aliases=["continue",'res'])
    async def resume(self, ctx):
        """resume audio"""
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            # print("resumed music")
            voice.resume()
        # else:
        #     print("music not paused")

    @commands.command(aliases=["vol"])
    async def volume(self, ctx):
        """sends volume instructions"""
        await ctx.send("> right click me to change volume.")


def setup(client):
    client.add_cog(Audio(client))
