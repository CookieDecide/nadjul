"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
import logging


async def join(ctx: commands.Context):
    """Bot joins the voice channel of the author.

    Args:
        ctx: Context of command invocation.
    """
    if ctx.voice_client is not None:
        logging.info(f"Bot moved to voice channel {ctx.author.voice.channel}")
        return await ctx.voice_client.move_to(ctx.author.voice.channel)

    await ctx.author.voice.channel.connect()
    logging.info(f"Bot joined voice channel {ctx.author.voice.channel}")


async def leave(ctx: commands.Context):
    """Stops and disconnects the bot from voice

    Args:
        ctx: Context of command invocation.
    """
    await ctx.voice_client.disconnect()
    logging.info(f"Bot disconnected from voice channel")


async def play(ctx: commands.Context, file_path):
    """Plays a file from the local filesystem

    Args:
        ctx: Context of command invocation.
        file_path: Path to the audio file.
    """
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(file_path))
    ctx.voice_client.play(
        source, after=lambda e: logging.info(f"Player error: {e}") if e else None
    )
    logging.info(f"Now playing: {file_path}")
    await ctx.send(f"Now playing: {file_path}")
