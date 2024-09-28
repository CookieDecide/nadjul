"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
Contains functions to gather animethemes.
"""

import requests
import urllib
import config
from config import logging
import os
from pathlib import Path

from model.db_anime import ANIME_TABLE, ANIMERESOURCES_TABLE, ANIMESERIES_TABLE, ANIMETHEMES_TABLE, ANIMEYEARS_TABLE, MALRATING_TABLE, ANIME_DB
import time
# https://api.animethemes.moe/anime?include=animethemes,series,animethemes.animethemeentries.videos.audio,images,studios,animethemes.song.artists,animethemes.song,resources

def gather_years():
    """Gathers the AnimeYears table from Animethemes.moe.

    Args:

    Returns:

    """
    url = "https://api.animethemes.moe/animeyear/"
    response = requests.get(url)
    data = response.json()

    logging.info(f"Inserting years into database.")

    for year in data:
        logging.debug(f"Inserting year {year}")
        ANIMEYEARS_TABLE.replace(
            year=year,
        ).execute()

        gather_animethemes(year)

    logging.info(f"Finished inserting years.")

def gather_animethemes(year: int):
    """Gathers the AnimeThemes table from Animethemes.moe for the given year.

    Args:
        year: Year to gather animethemes for.

    Returns:

    """
    pagesize = 100
    pagenumber = 1
    url = f"https://api.animethemes.moe/anime?include=animethemes,series,animethemes.animethemeentries.videos.audio,images,studios,animethemes.song.artists,animethemes.song,resources&filter[year]={year}&page[number]={pagenumber}&page[size]={pagesize}"

    while url != None:
        response = requests.get(url)
        data = response.json()
        url = data["links"]["next"]

        logging.debug(f"Inserting animethemes for year {year}, page {pagenumber}.")

        for anime in data["anime"]:
            if len(anime["series"]) > 0:
                ANIMESERIES_TABLE.replace(
                    id=anime["series"][0]["id"],
                    name=anime["series"][0]["name"],
                    slug=anime["series"][0]["slug"],
                ).execute()
                logging.debug(f"Inserted series {anime['series'][0]['name']}")

            # Special case for Fairy Tail, because the 2014 version has the same name as the 2009 version
            anime_name = anime["name"]
            if anime["id"] == 733 and anime["name"] == "Fairy Tail":
                anime_name = "Fairy Tail - 2014"

            ANIME_TABLE.replace(
                id=anime["id"],
                name=anime_name,
                media_format=anime["media_format"],
                season=anime["season"],
                slug=anime["slug"],
                synopsis=anime["synopsis"],
                year=anime["year"],
                img_url=anime["images"][0]["link"] if len(anime["images"]) > 0 else None,
                studio=anime["studios"][0]["name"] if len(anime["studios"]) > 0 else None,
                series=anime["series"][0]["id"] if len(anime["series"]) > 0 else None,
            ).execute()
            logging.debug(f"Inserted anime {anime['name']}")

            for resource in anime["resources"]:
                ANIMERESOURCES_TABLE.replace(
                    id=resource["id"],
                    external_id=resource["external_id"],
                    link=resource["link"],
                    site=resource["site"],
                    anime=anime["id"],
                ).execute()
                logging.debug(f"Inserted resource {resource['id']}")

                if resource["site"] == "MyAnimeList":
                    if MALRATING_TABLE.get_or_none(MALRATING_TABLE.resource == resource["id"]) == None:
                        resource["rating"], resource["scored_by"], resource["rank"], resource["popularity"], resource["favorites"], resource["members"] = get_mal_rating(resource["external_id"])
                        if resource["rating"] != None:
                            MALRATING_TABLE.replace(
                                anime=anime["id"],
                                rating=resource["rating"],
                                scored_by=resource["scored_by"],
                                rank=resource["rank"],
                                popularity=resource["popularity"],
                                favorites=resource["favorites"],
                                members=resource["members"],
                                resource=resource["id"],
                            ).execute()
                            logging.debug(f"Inserted malrating {resource['id']}")

            for theme in anime["animethemes"]:
                if len(theme["animethemeentries"]) > 0 and len(theme["animethemeentries"][0]["videos"]) > 0:
                    path  = Path(f"./{config.animethemes_output_path}{theme["animethemeentries"][0]["videos"][0]["audio"]["path"]}")
                    filepath = path.as_posix()
                    if(not os.path.exists(filepath)):
                        path.parent.mkdir(parents=True, exist_ok=True)

                        try:
                            urllib.request.urlretrieve(theme["animethemeentries"][0]["videos"][0]["audio"]["link"], filepath)
                        except Exception as e:
                            logging.warning(f"Failed to download {theme['animethemeentries'][0]['videos'][0]['audio']['link']} to {filepath}: {e}")
                            continue

                        logging.debug(f"Downloaded {theme['animethemeentries'][0]['videos'][0]['audio']['link']} to {filepath}")

                    ANIMETHEMES_TABLE.replace(
                        id=theme["id"],
                        sequence=theme["sequence"],
                        slug=theme["slug"],
                        type=theme["type"],
                        basename=theme["animethemeentries"][0]["videos"][0]["audio"]["basename"],
                        filename=theme["animethemeentries"][0]["videos"][0]["audio"]["filename"],
                        path=filepath,
                        size=theme["animethemeentries"][0]["videos"][0]["audio"]["size"],
                        link=theme["animethemeentries"][0]["videos"][0]["audio"]["link"],
                        song=theme["song"]["title"] if theme["song"] != None else None,
                        artist=theme["song"]["artists"][0]["name"] if (theme["song"] != None and len(theme["song"]["artists"]) > 0) else None,
                        anime=anime["id"],
                    ).execute()

                    logging.debug(f"Inserted animetheme {theme['id']}")

        pagenumber += 1

def get_mal_rating(anime_id: int):
    """Gets the rating of an anime from MyAnimeList.

    Args:
        anime_id: ID of the anime to get the rating for.

    Returns:
        Rating of the anime.
    """
    url = f"https://api.jikan.moe/v4/anime/{anime_id}"
    response = requests.get(url)
    if response.status_code == 429:
        # Rate limit exceeded, wait for a while and try again
        time.sleep(5)  # Wait for 5 seconds
        response = requests.get(url)

    if response.status_code != 200:
        logging.debug(f"Getting MAL rating for {anime_id}")
        logging.debug(f"Response: {response.text}")
        logging.debug(f"URL: {url}")
        logging.warning(f"Failed to get MAL rating for {anime_id}")
        return None, None, None, None, None, None

    data = response.json()
    data = data["data"]

    return data["score"], data["scored_by"], data["rank"], data["popularity"], data["favorites"], data["members"]