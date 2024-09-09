"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
import logging
import util.embed
import util.anime_gather
import threading


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

    def start_gathering():
        animeGathering = threading.Thread(target=util.anime_gather.gather_years)
        animeGathering.daemon = True
        animeGathering.start()

    @commands.command(name="ayaya", help="Ayayas.")
    async def ayaya(self, ctx: commands.Context):
        """Prints ayayo in the Chat.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received ayaya request from user {ctx.author}")
        await ctx.send("AYAYO!")
        logging.info(f"Finished ayaya request from user {ctx.author}")

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
