"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
import logging
import util.embed
import requests
import json


class BotNSFW(commands.Cog):
    """Collection of all NSFW commands and corresponding utility functions.

    Attributes:
        bot: Reference to discord bot.
    """

    def __init__(self, bot):
        """Initializes the instance.

        Args:
            bot: Discord bot.
        """
        self.bot = bot

    @commands.command(name="cat", help="Shows a random cat.")
    async def cat(self, ctx: commands.Context):
        """Shows a random cat.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received cat request from user {ctx.author}")

        cat = json.loads(
            requests.get("https://api.thecatapi.com/v1/images/search").text
        )[0]["url"]

        await ctx.send(
            embed=util.embed.create_embed_image(
                title="Cat",
                description="",
                img_url=cat,
                url=cat,
            )
        )

        logging.info(f"Finished cat request from user {ctx.author}")
