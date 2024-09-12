"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
Contains various helper functions and classes to receive content from xkcd.
"""

import urllib.request
import json
import random
from config import logging

_url_comic_current = "https://xkcd.com/info.0.json"
_url_comic_left = "https://xkcd.com/"
_url_comic_right = "/info.0.json"


class XkcdComic:
    """Represents a comic from xkcd.com. Currently only has title and image URL,
    might be changed in future.

    Attributes:
        title: Title of the comic.
        img_url: URL of the image of the comic.
        number: Number of the comic on website archive.
        url: URL pointing to comic (can be derived from comic number).
    """

    def __init__(self, title, img_url, number):
        self.title = title
        self.img_url = img_url
        self.number = number
        self.url = _url_comic_left + str(number) + "/"


def get_random_xkcd() -> XkcdComic:
    """Fetches a random comic from xkcd.com.
    API is described at https://xkcd.com/json.html

    Returns:
        XkcdComic: Valid comic object.
        None: Only returned when not able to fetch comic.
    """
    max_number = 0
    try:
        # Get current comic to derive maximum amount of available comics
        with urllib.request.urlopen(_url_comic_current) as url:
            data = json.load(url)
            max_number = data["num"]
            rand_number = random.randint(1, max_number)
            return create_xkcdcomic(rand_number)
    except urllib.error.HTTPError as err:
        logging.error(f"Exception occured: {err}")
        return None


def create_xkcdcomic(number) -> XkcdComic:
    """Fetches a comic from xkcd.com specified by its number.
    API is described at https://xkcd.com/json.html

    Returns:
        XkcdComic: Valid comic object.
        None: Only returned when not able to fetch comic.
    """
    url_comic = _url_comic_left + str(number) + _url_comic_right
    try:
        with urllib.request.urlopen(url_comic) as url:
            data = json.load(url)
            return XkcdComic(data["title"], data["img"], number)
    except urllib.error.HTTPError as err:
        logging.error(f"Exception occured: {err}")
        return None
