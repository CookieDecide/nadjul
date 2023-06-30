"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
import logging
import util.xkcd
import util.embed


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

    @commands.command(name="xkcd", help="Show a random comic from xkcd.com.")
    async def xkcd(self, ctx: commands.Context):
        """Shows a random xkcd comic. If not able to fetch one, shows an error message.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received xkcd request from user {ctx.author}")
        comic = util.xkcd.get_random_xkcd()
        if comic is None:
            logging.error("Not able to retrieve xkcd comic.")
            await ctx.send(
                embed=util.embed.create_embed_error("Not able to retrieve xkcd comic.")
            )
        else:
            await ctx.send(
                embed=util.embed.create_embed_image(
                    title="xkcd",
                    description=comic.title,
                    img_url=comic.img_url,
                    url=comic.url,
                )
            )
            logging.info(f"Finished xkcd request from user {ctx.author}")
