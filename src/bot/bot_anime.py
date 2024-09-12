"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
from config import logging
import util.embed
import util.anime_gather
import threading
import config
import asyncio
from resource_manager import shared_resources
from util.checks import is_dev


class BotAnime(commands.Cog):
    """Collection of all Anime commands and corresponding utility functions.

    Attributes:
        bot: Reference to discord bot.
    """
    def __init__(self, bot):
        """Initializes the instance.

        Args:
            bot: Discord bot.
        """
        self.bot = bot

    @commands.command(name="ayaya", help="Ayayas.")
    async def ayaya(self, ctx: commands.Context):
        """Prints ayayo in the Chat.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received ayaya request from user {ctx.author}")
        await ctx.send("AYAYO!")
        logging.info(f"Finished ayaya request from user {ctx.author}")

    @commands.command(name="aoq", help=".")
    async def start_quiz(self, ctx: commands.Context):
        """.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received start_quiz request from user {ctx.author}")

        audio_player = await config.resource_manager[ctx.guild.id].reserve(self, shared_resources.AUDIO_PLAYER)
        if audio_player is None:
            await ctx.send(embed=util.embed.create_embed_error("Audio player is already in use."))
            return
        
        await audio_player.join(ctx)
        await audio_player.play_local(ctx, "animethemes/2013/Spring/HatarakuMaouSama-OP1.ogg")
        await asyncio.sleep(5)
        audio_player.skip(ctx)
        
        await ctx.send("Started Quiz!")
        
        logging.info(f"Finished start_quiz request from user {ctx.author}")

    @commands.command(name="aoqstop", help=".")
    async def stop_quiz(self, ctx: commands.Context):
        """.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received stop_quiz request from user {ctx.author}")

        audio_player = await config.resource_manager[ctx.guild.id].check_ownership(self, shared_resources.AUDIO_PLAYER)
        if audio_player is None:
            await ctx.send(embed=util.embed.create_embed_error("Anime is not the owner of the audio player."))
            return

        await audio_player.leave(ctx)
        await ctx.send("Stopped Quiz!")

        await config.resource_manager[ctx.guild.id].free(self, shared_resources.AUDIO_PLAYER)

        logging.info(f"Finished stop_quiz request from user {ctx.author}")

    @start_quiz.before_invoke
    @stop_quiz.before_invoke
    async def acquire_lock(self, ctx):
        """Aquires the audio player lock.

        Args:
            ctx: Context of command invocation.
        """
        audio_player_lock = config.resource_manager[ctx.guild.id].acquire_lock(shared_resources.AUDIO_PLAYER)
        await audio_player_lock.acquire()

    @start_quiz.after_invoke
    @stop_quiz.after_invoke
    async def release_lock(self, ctx):
        """Releases the audio player lock.

        Args:
            ctx: Context of command invocation.
        """
        audio_player_lock = config.resource_manager[ctx.guild.id].acquire_lock(shared_resources.AUDIO_PLAYER)
        audio_player_lock.release()

    @commands.check(is_dev)
    @commands.command(name="uat", help="Updates the AnimeThemes.", hidden=True)
    async def update_anime_themes(self, ctx: commands.Context):
        """Starts the Thread to update the Database of AnimeThemes.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received uat request from user {ctx.author}")
        animeGathering = threading.Thread(target=util.anime_gather.gather_years)
        animeGathering.daemon = True
        animeGathering.start()
        logging.info(f"Finished uat request from user {ctx.author}")
