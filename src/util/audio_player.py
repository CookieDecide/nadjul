"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
import logging
import util.embed
import asyncio
from random import shuffle
from util.yt_download import parse_playlist, download

queue = []
is_playing = False


async def join(ctx: commands.Context):
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


async def leave(ctx: commands.Context):
    """Stops and disconnects the bot from voice

    Args:
        ctx: Context of command invocation.
    """
    await ctx.voice_client.disconnect()
    logging.info(f"Bot disconnected from voice channel")


async def play(ctx: commands.Context, url):
    """Plays a file from the local filesystem.

    Args:
        ctx: Context of command invocation.
        url: The Youtube url.
    """
    if "list" in url:
        for song in parse_playlist(url):
            await queue_append(ctx, song)
    else:
        await queue_append(ctx, url)

    if not is_playing:
        await play_loop(ctx)


async def queue_append(ctx: commands.Context, url):
    """Appends the given file to the queue.

    Args:
        ctx: Context of command invocation.
        url: The Youtube url.
    """
    queue.append(url)


async def play_loop(ctx: commands.Context):
    """Plays the next song in the queue. Continues with the next song if available or ends.

    Args:
        ctx: Context of command invocation.
    """
    global is_playing
    if len(queue) > 0:
        is_playing = True
        next_file = download(queue.pop(0))
        if next_file == None:
            await play_loop(ctx)
            return

        next_filepath = next_file.filepath + next_file.filename
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source=next_filepath))

        await ctx.send(f"Now playing: {next_file.title}")

        logging.info(f"Now playing: {next_file}")
        ctx.voice_client.play(source)
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        await play_loop(ctx)
    else:
        is_playing = False
        await leave(ctx)


def skip(ctx):
    """Skips the current song.

    Args:
        ctx: Context of command invocation.
    """
    ctx.voice_client.stop()


def clear_queue():
    """Clears the song queue.

    Args:
        ctx: Context of command invocation.
    """
    queue.clear()


def get_queue() -> list:
    """Returns the song queue.

    Args:
        ctx: Context of command invocation.

    Returns:
        queue: Current song queue.
    """
    return queue


def shuffle_queue():
    """Shuffles the song queue.

    Args:
        ctx: Context of command invocation.
    """
    shuffle(queue)
