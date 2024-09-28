"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""
import discord
from discord.ext import commands
from config import logging
import util.embed
import config
from resource_manager import shared_resources


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
        
    @commands.hybrid_command(name="play", help="Plays the provided YouTube url.")
    async def play(self, ctx: commands.Context, url):
        """Plays the provided YouTube url.

        Args:
            ctx: Context of command invocation.
            url: Url of the YouTube video.
        """
        logging.info(f"Received play request from user {ctx.author}")

        audio_player = await config.resource_manager[ctx.guild.id].reserve(self, shared_resources.AUDIO_PLAYER)
        if audio_player is None:
            await ctx.send(embed=util.embed.create_embed_error("Audio player is already in use."))
            return

        await audio_player.play_yt(ctx, url)

        logging.info(f"Finished play request from user {ctx.author}")

    @commands.hybrid_command(name="stop", help="Stops the current song.")
    async def stop(self, ctx: commands.Context):
        """Stops the current song.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received stop request from user {ctx.author}")

        audio_player = await config.resource_manager[ctx.guild.id].check_ownership(self, shared_resources.AUDIO_PLAYER)
        if audio_player is None:
            await ctx.send(embed=util.embed.create_embed_error("Music is not the owner of the audio player."))
            return

        await audio_player.clear_queue()
        audio_player.skip(ctx)
        
        await config.resource_manager[ctx.guild.id].free(self, shared_resources.AUDIO_PLAYER)

        logging.info(f"Finished stop request from user {ctx.author}")

    @commands.hybrid_command(name="skip", help="Skips the current song.")
    async def skip(self, ctx: commands.Context):
        """Skips the current song.

        Args:
            ctx: Context of command invocation.
        """
        audio_player = await config.resource_manager[ctx.guild.id].check_ownership(self, shared_resources.AUDIO_PLAYER)
        if audio_player is None:
            await ctx.send(embed=util.embed.create_embed_error("Music is not the owner of the audio player."))
            return
        
        audio_player.skip(ctx)

    @commands.hybrid_command(name="queue", help="Sends the current song queue.")
    async def print_queue(self, ctx: commands.Context):
        """Sends the current song queue.

        Args:
            ctx: Context of command invocation.
        """
        audio_player = await config.resource_manager[ctx.guild.id].check_ownership(self, shared_resources.AUDIO_PLAYER)
        if audio_player is None:
            await ctx.send(embed=util.embed.create_embed_error("Music is not the owner of the audio player."))
            return
        
        queue = audio_player.get_queue()
        await ctx.send(embed=util.embed.create_embed_queue(queue))

    @commands.hybrid_command(name="shuffle", help="Shuffles the song queue.")
    async def shuffle_queue(self, ctx: commands.Context):
        """Shuffles the song queue.

        Args:
            ctx: Context of command invocation.
        """
        audio_player = await config.resource_manager[ctx.guild.id].check_ownership(self, shared_resources.AUDIO_PLAYER)
        if audio_player is None:
            await ctx.send(embed=util.embed.create_embed_error("Music is not the owner of the audio player."))
            return
        
        await audio_player.shuffle_queue()
        queue = util.audio_player.get_queue()
        await ctx.send(embed=util.embed.create_embed_queue(queue))

    @play.before_invoke
    @stop.before_invoke
    @skip.before_invoke
    @print_queue.before_invoke
    @shuffle_queue.before_invoke
    async def acquire_lock(self, ctx):
        """Aquires the audio player lock.

        Args:
            ctx: Context of command invocation.
        """
        audio_player_lock = config.resource_manager[ctx.guild.id].acquire_lock(shared_resources.AUDIO_PLAYER)
        await audio_player_lock.acquire()

    @play.after_invoke
    @stop.after_invoke
    @skip.after_invoke
    @print_queue.after_invoke
    @shuffle_queue.after_invoke
    async def release_lock(self, ctx):
        """Releases the audio player lock.

        Args:
            ctx: Context of command invocation.
        """
        audio_player_lock = config.resource_manager[ctx.guild.id].acquire_lock(shared_resources.AUDIO_PLAYER)
        audio_player_lock.release()

