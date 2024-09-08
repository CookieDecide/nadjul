"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
Contains various helper functions to create embeds for sending. 
Assures consistent look over different modules.
"""

import discord
from discord.ext import commands
from util.yt_download import get_title


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
        description += str(i) + ". " + get_title(song) + "\n"
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
