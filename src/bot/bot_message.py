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

        total_deleted = 0

        for i in range(0, (count // 100) + 1):
            deleted = len(await ctx.channel.purge(limit=100))
            total_deleted += deleted
            if deleted < 100:
                break

        await ctx.send(f"Deleted {total_deleted} messages.")

        logging.info(f"Purged {i+1} times.")
        logging.info(f"Finished purge request from user {ctx.author}")
