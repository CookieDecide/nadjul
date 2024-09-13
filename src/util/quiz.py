"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
import asyncio
import util.embed

async def gather_players(ctx, lobby, title):
    """Gather players for the lobby.

    Args:
        ctx: Context of command invocation.
        lobby: Lobby to gather players for.
    """
    await ctx.send(embed=util.embed.create_embed_lobby_join(title))
    while not lobby.is_full():
        try:
            msg = await ctx.bot.wait_for("message", check=lambda m: m.content == "join" and m.author != ctx.bot.user, timeout=10)
            if not lobby.add_player(msg.author.id):
                await ctx.send(f"{msg.author.mention} Lobby is full.")
            else:
                await ctx.send(f"{msg.author.mention} joined the lobby.")
        except asyncio.TimeoutError:
            break
    await ctx.send("Registration is closed!")

    await ctx.send(embed=util.embed.create_embed_list(title, "Players:", [ctx.guild.get_member(player_id).mention for player_id in lobby.get_players()]))

async def prepare_quiz(ctx, quiz_title):
    """Prepare the quiz.

    Args:
        ctx: Context of command invocation.
        quiz_title: Title of the quiz
    """
    await ctx.send(embed=discord.Embed(title=quiz_title, description="Quiz starting in 5 seconds!", color = 0x14D8FA))
    await asyncio.sleep(5)
    await ctx.send(embed=discord.Embed(title=quiz_title, description="Quiz starting now!", color = 0x14D8FA))