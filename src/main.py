import discord
from discord.ext import commands
from api_key import __api_key__
import asyncio
import config

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config.command_prefix),
    description=config.bot_description,
    intents=intents,
)

@bot.command(name="helloworld")
async def hello_world(ctx):
    """Send 'Hello World!'"""
    await ctx.send("Hello World!")  

async def main():
    async with bot:
        await bot.start(__api_key__)

asyncio.run(main())
