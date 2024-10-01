"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
Contains various helper functions to create embeds for sending. 
Assures consistent look over different modules.
"""

import discord
from discord.ext import commands
from util.yt_download import get_title
from config import logging


def create_embed_image(title, description, img_url, url) -> discord.Embed:
    """Creates an embed showing an image.

    Args:
        title: Title of the embed.
        description: Description/Message of embed.
        img_url: URL pointing to the image.
        url: URL pointing to the webpage the image is embedded on.
             If not existing, provide img_url here.

    Returns:
        An embed with blue color showing an image.
    """
    color = 0x14D8FA  # blue
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        url=url,
    )
    embed.set_image(url=img_url)

    return embed


def create_embed_error(description) -> discord.Embed:
    """Creates an embed indicating and error.

    Args:
        description: Description/Message of embed.

    Returns:
        An embed with red color including an error message.
    """
    color = 0xFF0000  # red
    embed = discord.Embed(
        title="Error",
        description=description,
        color=color,
    )

    return embed


def create_embed_queue(queue) -> discord.Embed:
    """Creates an embed indicating and error.

    Args:
        description: Description/Message of embed.

    Returns:
        An embed with red color including an error message.
    """
    if len(queue) == 0:
        return create_embed_error("Queue is empty!")

    description = ""
    i = 0
    for song in queue:
        title = ""
        if "youtube" in song:
            title = get_title(song)
        else:
            title = song

        description += str(i) + ". " + title + "\n"
        if i >= 9:
            break
        i += 1

    color = 0x14D8FA  # blue
    embed = discord.Embed(
        title="Song Queue:",
        description=description,
        color=color,
    )

    return embed


def create_embed_lobby_join(lobby_name: str) -> discord.Embed:
    """Creates an embed for joining a lobby.

    Args:
        lobby_name: Name of the lobby.

    Returns:
        An embed with blue color showing the lobby.
    """
    color = 0x14D8FA  # blue
    embed = discord.Embed(
        title=lobby_name,
        description=f"To join the lobby, write 'join' in the chat.",
        color=color,
    )

    return embed

def create_embed_list(title, description, items) -> discord.Embed:
    """Creates an embed showing a list.

    Args:
        title: Title of the embed.
        description: Description/Message of embed.
        items: List of items to show.

    Returns:
        An embed with blue color showing a list.
    """
    for i, item in enumerate(items):
        description += f"\n{i+1}. {item}"

    color = 0x14D8FA  # blue
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )

    return embed

def create_embed_dict(title, description, items) -> discord.Embed:
    """Creates an embed showing a dictionary.

    Args:
        title: Title of the embed.
        description: Description/Message of embed.
        items: Dictionary of items to show.

    Returns:
        An embed with blue color showing a dictionary.
    """
    for key, value in items.items():
        description += f"\n{key}: {value}"

    color = 0x14D8FA  # blue
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )

    return embed

def create_embed_aoq_quiz(title, description, items, hint) -> discord.Embed:
    """Creates an embed showing a quiz.

    Args:
        title: Title of the embed.
        description: Description/Message of embed.
        items: Dictionary of items to show.

    Returns:
        An embed with blue color showing a quiz.
    """
    if hint != "":
        description += f"\n{hint}"
    color = 0x14D8FA  # blue
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )

    i=0
    for item in items:
        embed.add_field(name=f"{i+1}:\t{item.anime.name}-{item.slug}", value="", inline=False)
        i+=1

    return embed

def create_embed_scoreboard(ctx, title, description, items) -> discord.Embed:
    """Creates an embed showing a scoreboard.

    Args:
        title: Title of the embed.
        description: Description/Message of embed.
        items: Dictionary of items to show.

    Returns:
        An embed with blue color showing a scoreboard.
    """
    print(items)
    color = 0x14D8FA  # blue
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )

    i=0
    for key, value in sorted(items.items(), key=lambda item: item[1], reverse=True):
        embed.add_field(name=f"{i+1}:\t{ctx.guild.get_member(key)}\t{value}", value=f"", inline=False)
        i+=1

    return embed

def create_embed_aop_solution(title, description, solution) -> discord.Embed:
    """Creates an embed showing the solution of a quiz.

    Args:
        title: Title of the embed.
        description: Description/Message of embed.
        items: Dictionary of items to show.

    Returns:
        An embed with blue color showing the solution of a quiz.
    """
    color = 0x14D8FA  # blue
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )

    embed.add_field(name=f"Solution:\t{solution.anime.name}-{solution.slug}", value=f"", inline=False)

    return embed

def create_embed_aoq_fastest(title, description) -> discord.Embed:
    """Creates an embed showing the fastest answer of a quiz.

    Args:
        title: Title of the embed.
        description: Description/Message of embed.
        items: Dictionary of items to show.

    Returns:
        An embed with blue color showing the fastest answer of a quiz.
    """
    color = 0x14D8FA  # blue
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
    )

    return embed