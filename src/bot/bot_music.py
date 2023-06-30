"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
import logging
import util.embed
import util.audio_player
import util.yt_download


class BotMusic(commands.Cog):
    """Collection of all Music commands and corresponding utility functions.

    Attributes:
        bot: Reference to discord bot.
    """

    def __init__(self, bot):
        """Initializes the instance.

        Args:
            bot: Discord bot.
        """
        self.bot = bot

    @commands.command(name="play", help="Plays the provided YouTube url.")
    async def play(self, ctx: commands.Context, url):
        """Plays the provided YouTube url.

        Args:
            ctx: Context of command invocation.
            url: Url of the YouTube video.
        """
        logging.info(f"Received play request from user {ctx.author}")

        audio = util.yt_download.download(url)

        await util.audio_player.join(ctx)
        await util.audio_player.play(ctx, audio)

        logging.info(f"Finished play request from user {ctx.author}")

    @commands.command(name="stop", help="Stops the current song.")
    async def stop(self, ctx: commands.Context):
        """Stops the current song.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received stop request from user {ctx.author}")

        util.audio_player.clear_queue()
        util.audio_player.skip(ctx)
        await util.audio_player.leave(ctx)

        logging.info(f"Finished stop request from user {ctx.author}")

    @commands.command(name="skip", help="Skips the current song.")
    async def skip(self, ctx: commands.Context):
        """Skips the current song.

        Args:
            ctx: Context of command invocation.
        """
        util.audio_player.skip(ctx)

    @commands.command(name="queue", help="Sends the current song queue.")
    async def print_queue(self, ctx: commands.Context):
        """Sends the current song queue.

        Args:
            ctx: Context of command invocation.
        """
        queue = util.audio_player.get_queue()
        await ctx.send(embed=util.embed.create_embed_queue(queue))
