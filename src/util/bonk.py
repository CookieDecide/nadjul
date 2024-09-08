"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
Contains helper functions to create bonk images.
"""

import requests
from PIL import Image
import config
import logging


def create_bonk_img(avatar_url) -> Image.Image:
    """Creates a bonk image withe the given discord avatar.

    Args:
        avatar_url: Url to the users avatar.

    Returns:
        Image of the avatar being bonked.
    """
    bonk = Image.open(config.img_path + "bonk.png")

    avatar = Image.open(
        requests.get(
            avatar_url,
            stream=True,
        ).raw
    )
    avatar = avatar.resize((256, 256))

    bonk.paste(avatar, (700, 400))

    return bonk
