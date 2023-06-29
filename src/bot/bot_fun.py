"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
import logging


class BotFun(commands.Cog):
    """Collection of all Fun commands and corresponding utility functions.

    Attributes:
        bot: Reference to discord bot.
    """

    def __init__(self, bot):
        """Initializes the instance.

        Args:
            bot: Discord bot.
        """
        self.bot = bot

    @commands.command(name="ping", help="Returns pong.")
    async def ping(self, ctx: commands.Context):
        """Sends a pong message.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received ping request from user {ctx.author}")
        await ctx.send("Pong!")
        logging.info(f"Finished ping request from user {ctx.author}")
