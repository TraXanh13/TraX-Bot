import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.isPlaying = False
        self.isPaused = False

        self.musicQueue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def searchYoutube(self, query):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)[
                    'entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def playNext(self, ctx):
        if (len(self.musicQueue) > 0):
            self.isPlaying = True
            self.isPaused = False

            self.musicQueue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(
                self.musicQueue[0][1], **self.FFMPEG_OPTIONS), after=lambda e: self.playNext(ctx))
        else:
            self.isPlaying = False
            self.isPaused = False

    async def playMusic(self, ctx):
        if len(self.musicQueue) > 0:
            self.isPlaying = True
            songURL = self.musicQueue[0][0]['source']

            if self.vc == None or not self.vb.is_connected():
                self.vc = await self.musicQueue[0][1].connect()

                if self.vc == None:
                    await ctx.send("I cannot connect to the voice channel.")
                    return
            else:
                await self.vc.move_to(self.musicQueue[0][1])

            self.musicQueue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(
                songURL, **self.FFMPEG_OPTIONS), after=lambda e: self.playNext(ctx))

        else:
            self.isPlaying = False

    @commands.command(name="play", aliases=["mp"], help="Plays a song from YouTube.")
    async def play(self, ctx, *args):
        query = " ".join(args)

        vc = ctx.message.author.voice.channel
        if vc == None:
            await ctx.send("You are not connected to a voice channel.")
            return
        elif self.isPaused:
            self.vc.resume()
            self.isPaused = False
            return
        else:
            song = self.searchYoutube(query)

            if song == False:
                await ctx.send("Could not find the song.")
                return

            await ctx.send(f"Added {song['title']} to the queue.")
            self.musicQueue.append([song, vc])

            if self.isPlaying == False:
                await self.playMusic(ctx)

    @commands.command(name="pause", help="Pauses the current song.")
    async def pause(self, ctx):
        if self.vc.is_playing():
            self.vc.pause()
            self.isPaused = True
            self.isPlaying = False

    @commands.command(name="resume", help="Resumes the current song.")
    async def resume(self, ctx):
        if self.vc.is_paused():
            self.vc.resume()
            self.isPaused = False
            self.isPlaying = True

    @commands.command(name="skip", help="Skips the current song.")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.playMusic(ctx)

    @commands.command(name="queue", aliases=["mq"], help="Shows the current queue.")
    async def queue(self, ctx):
        if len(self.musicQueue) > 0:
            queueMsg = "Current queue:\n"

            for i in range(len(self.musicQueue)):
                if i > 10:
                    queueMsg += f"and {len(self.musicQueue) - 10} more..."
                    break
                queueMsg += f"{i+1}. {self.musicQueue[i][0]['title']}\n"

            await ctx.send(queueMsg)
        else:
            await ctx.send("There are no songs in the queue.")

    @commands.command(name="stop", help="Stops the music and clears the queue.")
    async def stop(self, ctx):
        if self.vc != None and self.isPlaying:
            self.vc.stop()
        self.musicQueue.clear()
        self.isPlaying = False
        self.isPaused = False

    @commands.command(name="clear", help="Clears the queue.")
    async def clear(self, ctx):
        self.musicQueue.clear()
        await ctx.send("Cleared the music queue.")

    @commands.command(name="leave", help="Leaves the voice channel.")
    async def leave(self, ctx):
        if self.vc != None and self.vc.is_connected():
            await self.vc.disconnect()
            self.vc = None
            self.isPlaying = False
            self.isPaused = False


async def setup(client):
    await client.add_cog(music(client))
