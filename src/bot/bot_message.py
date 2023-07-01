"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
import logging
import util.embed


class BotMessage(commands.Cog):
    """Collection of all Message commands and corresponding utility functions.

    Attributes:
        bot: Reference to discord bot.
    """

    def __init__(self, bot):
        """Initializes the instance.

        Args:
            bot: Discord bot.
        """
        self.bot = bot

    @commands.command(name="purge", help="Deletes the last x messages.")
    async def purge(self, ctx: commands.Context, count: int):
        """Deletes the last x messages.

        Args:
            ctx: Context of command invocation.
            count: Number of messages to delete.
        """
        logging.info(f"Received purge request from user {ctx.author}")

        deleted = 0
        to_delete = count
        while to_delete > 100:
            await ctx.channel.purge(limit=100)
            deleted = deleted + 100
            to_delete = to_delete - 100
        deleted_smaller_100 = await ctx.channel.purge(limit=to_delete)
        deleted = deleted + len(deleted_smaller_100)

        await ctx.send(f"Deleted {deleted} messages.")

        logging.info(f"Finished purge request from user {ctx.author}")
