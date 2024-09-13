"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
from config import logging
import util.embed
import asyncio
from random import shuffle
from util.yt_download import parse_playlist, download
import config
import os

class TrackableQueue(asyncio.Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._all_items = []  # List to track all items added to the queue

    async def put(self, item):
        """Override the put method to track all items."""
        await super().put(item)
        self._all_items.append(item)

    async def get(self):
        """Override the get method to remove items from the tracking list."""
        item = await super().get()
        self._all_items.remove(item)
        return item

    def get_all_items(self):
        """Return all items that have been added without removing them."""
        return self._all_items
    
    async def shuffle(self):
        """Shuffle the queue while maintaining the correct order."""
        # Step 1: Dequeue all items from the original queue
        items = []
        while not self.empty():
            items.append(await super().get())
        
        # Step 2: Shuffle the items
        shuffle(items)
        
        # Step 3: Re-enqueue the shuffled items and update _all_items
        self._all_items = items  # Update the tracked list
        for item in items:
            await super().put(item)

class AudioPlayer:
    __queue = TrackableQueue()
    __play_loop_task = None
    lock: asyncio.Lock
    
    def __init__(self, lock: asyncio.Lock):
        """Initializes the instance.
        """
        self.lock = lock

    async def join(self, ctx: commands.Context):
        """Bot joins the voice channel of the author.

        Args:
            ctx: Context of command invocation.
        """
        if ctx.voice_client is not None:
            logging.info(f"Bot moved to voice channel {ctx.author.voice.channel}")
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            logging.info(f"Bot joined voice channel {ctx.author.voice.channel}")
        else:
            await ctx.send(
                embed=util.embed.create_embed_error(
                    "You are not connected to a voice channel."
                )
            )

            logging.info(f"Author not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")


    async def leave(self, ctx: commands.Context):
        """Stops and disconnects the bot from voice

        Args:
            ctx: Context of command invocation.
        """
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        if self.__play_loop_task != None:
            self.__play_loop_task.cancel()
        logging.info(f"Bot disconnected from voice channel")


    async def play_yt(self, ctx: commands.Context, url: str):
        """Adds an Entry to the Queue.

        Args:
            ctx: Context of command invocation.
            url: The Youtube url.
        """
        if "list" in url:
            for song in parse_playlist(url):
                await self.__queue.put(song)
        else:
            await self.__queue.put(url)
            

        if self.__play_loop_task == None or self.__play_loop_task.done():
            self.__play_loop_task = asyncio.create_task(self.__play_loop(ctx))

    async def __play_loop(self, ctx: commands.Context):
        """Plays the next song in the queue. Continues with the next song if available or ends.

        Args:
            ctx: Context of command invocation.
        """
        while True:
            work = await self.__queue.get()  # Wait for a song to be added to the queue
            await self.join(ctx)

            await self.play_yt_song(ctx, work)
            
            self.__queue.task_done()  # Mark the song as processed

            # If the queue is empty after playing, release the reservation
            async with self.lock:
                if self.__queue.empty():
                    await config.resource_manager[ctx.guild.id].free_resource_self(self)
                    await self.leave(ctx)
                    return

    async def play_yt_song(self, ctx: commands.Context, url: str):
        """Plays a song from youtube.

        Args:
            ctx: Context of command invocation.
            url: The Youtube url.
        """
        try:
            song = download(url)
            next_filepath = song.filepath + song.filename
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=next_filepath))

            await ctx.send(f"Now playing: {song.title}")
            logging.info(f"Now playing: {song}")

            ctx.voice_client.play(source)
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)
        except Exception as e:
            await ctx.send(embed=util.embed.create_embed_error(f"Error while playing song: {url}"))
            logging.error(f"Error while playing song: {e}")

    async def play_local(self, ctx: commands.Context, path: str):
        """Plays a file from the local filesystem.

        Args:
            ctx: Context of command invocation.
            filename: The filename of the file to play.
        """
        if not os.path.exists(path):
            await ctx.send(embed=util.embed.create_embed_error(f"File {path} does not exist."))
            logging.error(f"File {path} does not exist.")
            return
        
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=path))

        # await ctx.send(f"Now playing: {path}")
        logging.info(f"Now playing: {path}")

        ctx.voice_client.play(source)

    def skip(self, ctx):
        """Skips the current song.

        Args:
            ctx: Context of command invocation.
        """
        ctx.voice_client.stop()


    async def clear_queue(self):
        """Clears the song queue.

        Args:
            ctx: Context of command invocation.
        """
        while not self.__queue.empty():
            await self.__queue.get()
            self.__queue.task_done()


    def get_queue(self) -> list:
        """Returns the song queue.

        Args:
            ctx: Context of command invocation.

        Returns:
            queue: Current song queue.
        """
        return self.__queue.get_all_items()


    async def shuffle_queue(self):
        """Shuffles the song queue.

        Args:
            ctx: Context of command invocation.
        """
        await self.__queue.shuffle()
