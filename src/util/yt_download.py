"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

from pytube import YouTube
from pytube import Playlist
import logging
import time
import hashlib
import config
import os

from model.db_audio import YOUTUBE_TABLE


def __download_single(url):
    """Downloads the audio of the given url. Should not be called from outside, use download() instead.

    Args:
        url: Youtube url of the video.

    Returns:
        The database entry of the video.
    """
    if not os.path.exists(config.youtube_output_path):
        os.mkdir(config.youtube_output_path)

    if is_url_downloaded_single(url):
        logging.info(f"Url {url} is already downloaded")
    else:
        logging.info(f"Started download for url {url}")
        video = YouTube(url)
        filename = video.video_id + "." + config.youtube_file_extension
        video.streams.filter(
            file_extension=config.youtube_file_extension, only_audio=True
        ).first().download(output_path=config.youtube_output_path, filename=filename)

        YOUTUBE_TABLE.insert(
            url=url,
            title=video.title,
            length=video.length,
            filepath=config.youtube_output_path,
            filename=filename,
            thumbnail_url=video.thumbnail_url,
            timestamp=int(time.time()),
            hash_=compute_hash(config.youtube_output_path + filename),
        ).execute()

        logging.info(f"Finished download for url {url}")
        logging.info(f"Saved file in {config.youtube_output_path + filename}")

    return YOUTUBE_TABLE.get(YOUTUBE_TABLE.url == url)


def __download_playlist(url):
    """Downloads the audio of the given playlist url. Should not be called from outside, use download() instead.

    Args:
        url: Youtube url of the playlist.
    """
    logging.info(f"Started download for playlist url {url}")
    playlist = Playlist(url)
    logging.info(f"Number of videos in playlist: {playlist.length}")

    index = 0
    for video_url in playlist.video_urls:
        index += 1
        __download_single(video_url)
        logging.info(f"Finished download for video nr. {index}")

    logging.info(f"Finished download for playlist url {url}")


def download(url):
    """Downloads the audio of the given url.

    Args:
        url: Youtube url of the video.

    Returns:
        The database entry of the video.
    """
    if "list" in url:
        return __download_playlist(url)
    else:
        return __download_single(url)


def is_url_downloaded_single(url):
    """Checks if the given url is already downloaded.

    Args:
        url: Youtube url of the video.

    Returns:
        bool: true - url already downloaded
    """
    logging.info(f"Checking url {url}")

    if YOUTUBE_TABLE.get_or_none(YOUTUBE_TABLE.url == url):
        return True

    return False


def compute_hash(filepath):
    """Compute the sha3_256_hash of a given mp4 file.

    Args:
        filepath: Filepath of the mp4 file.

    Returns:
        string: readable_hash - sha3_256_hash of the given mp4 file
    """
    logging.info(f"Computing hash for file {filepath}")

    sha3_256_hash = hashlib.sha3_256()
    with open(filepath, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha3_256_hash.update(byte_block)
        readable_hash = sha3_256_hash.hexdigest()
        logging.info(f"Generated sha3_256_hash {readable_hash}")

    return readable_hash
