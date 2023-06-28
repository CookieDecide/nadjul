"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
from api_key import __api_key__
import asyncio
import config
import apps.fun

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config.command_prefix),
    description=config.bot_description,
    intents=intents,
)

async def main():
    async with bot:
        await bot.add_cog(apps.fun.Fun(bot))

        await bot.start(__api_key__)

asyncio.run(main())
