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
from bot.bot_fun import BotFun
from bot.bot_music import BotMusic
from bot.bot_message import BotMessage
from bot.bot_nsfw import BotNSFW

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
        + "all_"
        + time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        + ".log"
    )

    # Create log folder if does not exist
    if not os.path.exists(config.log_path):
        os.makedirs(config.log_path)

    # Configure root logger in logging
    logging.basicConfig(filename=filename, format=format, level=level)


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game("Try >help")
    )
    logging.info(f"Logged in as {bot.user} ({bot.user.id})")
    print("Logged in as {0} ({0.id})".format(bot.user))
    print("------")


async def main():
    async with bot:
        logging.info("Adding modules to bot")
        await bot.add_cog(BotFun(bot))
        await bot.add_cog(BotMusic(bot))
        await bot.add_cog(BotMessage(bot))
        await bot.add_cog(BotNSFW(bot))
        logging.info("Modules added")

        logging.info("Starting bot")
        await bot.start(__api_key__)


abspath = os.path.abspath(__file__ + "/..")
dname = os.path.dirname(abspath)
os.chdir(dname)

init_log()
asyncio.run(main())
