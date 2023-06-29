"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
from api_key import __api_key__
import asyncio
import config
import os
import logging
import time
import apps.fun

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config.command_prefix),
    description=config.bot_description,
    intents=intents,
)


def init_log():
    # Log messages should look like: [LEVEL] time - module:func - message
    format = "[%(levelname)s] %(asctime)s - %(module)s:%(funcName)s - %(message)s"
    level = logging.INFO
    filename = (
        config.log_path
        + "main_"
        + time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        + ".log"
    )

    # Create log folder if does not exist
    if not os.path.exists(config.log_path):
        os.makedirs(config.log_path)

    # Configure root logger in logging
    logging.basicConfig(filename=filename, format=format, level=level)


async def main():
    async with bot:
        logging.info("Adding modules to bot")
        await bot.add_cog(apps.fun.Fun(bot))
        logging.info("Modules added")

        logging.info("Starting bot")
        await bot.start(__api_key__)


init_log()
asyncio.run(main())
