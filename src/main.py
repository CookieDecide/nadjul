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
from bot.bot_anime import BotAnime
from resource_manager import ResourceManager

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config.command_prefix),
    description=config.bot_description,
    intents=intents,
)


def init_log():
    # Log messages should look like: [LEVEL] time - module:func - message
    format = "[%(levelname)s] %(asctime)s - %(module)s:%(funcName)s - %(message)s"

    # Create log folder if does not exist
    if not os.path.exists(config.log_path):
        os.makedirs(config.log_path)

    # Create a logger
    logger = logging.getLogger("application")
    logger.setLevel(logging.DEBUG)  # Set the overall logging level

    # Create file handlers
    filename = (
        config.log_path
        + "all_"
        + "info_"
        + time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        + ".log"
    )
    info_handler = logging.FileHandler(filename=filename, encoding="utf-8")
    info_handler.setLevel(logging.INFO)  # Only INFO and above go to info.log

    filename = (
        config.log_path
        + "all_"
        + "debug_"
        + time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        + ".log"
    )
    debug_handler = logging.FileHandler(filename=filename, encoding="utf-8")
    debug_handler.setLevel(logging.DEBUG)  # DEBUG and above go to debug.log

    # Create a formatter and set it for the handlers
    formatter = logging.Formatter(format)
    info_handler.setFormatter(formatter)
    debug_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(debug_handler)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        config.logging.info(f"Connected to guild {guild.name} ({guild.id})")
        print(f"Connected to guild {guild.name} ({guild.id})")
        config.resource_manager[guild.id] = ResourceManager()

    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game("Try >help")
    )
    config.logging.info(f"Logged in as {bot.user} ({bot.user.id})")
    print("Logged in as {0} ({0.id})".format(bot.user))
    print("------")

@bot.event
async def on_guild_join(guild):
    print(f"Joined guild {guild.name} ({guild.id})")
    config.resource_manager[guild.id] = ResourceManager()


async def main():
    async with bot:
        config.logging.info("Adding modules to bot")
        await bot.add_cog(BotFun(bot))
        await bot.add_cog(BotMusic(bot))
        await bot.add_cog(BotMessage(bot))
        await bot.add_cog(BotNSFW(bot))
        await bot.add_cog(BotAnime(bot))
        config.logging.info("Modules added")

        config.logging.info("Starting bot")
        await bot.start(__api_key__)


abspath = os.path.abspath(__file__ + "/..")
dname = os.path.dirname(abspath)
os.chdir(dname)

init_log()
asyncio.run(main())
