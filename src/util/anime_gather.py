"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
Contains functions to gather animethemes.
"""

import requests
import urllib
import config
import logging
import os
from pathlib import Path

from model.db_anime import ANIME_TABLE, ANIMERESOURCES_TABLE, ANIMESERIES_TABLE, ANIMETHEMES_TABLE, ANIMEYEARS_TABLE, ANIME_DB
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
        logging.info(f"Inserting year {year}")
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

        logging.info(f"Inserting animethemes for year {year}, page {pagenumber}.")

        for anime in data["anime"]:
            if len(anime["series"]) > 0:
                ANIMESERIES_TABLE.replace(
                    id=anime["series"][0]["id"],
                    name=anime["series"][0]["name"],
                    slug=anime["series"][0]["slug"],
                ).execute()
                logging.info(f"Inserted series {anime['series'][0]['name']}")

            ANIME_TABLE.replace(
                id=anime["id"],
                name=anime["name"],
                media_format=anime["media_format"],
                season=anime["season"],
                slug=anime["slug"],
                synopsis=anime["synopsis"],
                year=anime["year"],
                img_url=anime["images"][0]["link"] if len(anime["images"]) > 0 else None,
                studio=anime["studios"][0]["name"] if len(anime["studios"]) > 0 else None,
                series=anime["series"][0]["id"] if len(anime["series"]) > 0 else None,
            ).execute()
            logging.info(f"Inserted anime {anime['name']}")

            for resource in anime["resources"]:
                ANIMERESOURCES_TABLE.replace(
                    id=resource["id"],
                    external_id=resource["external_id"],
                    link=resource["link"],
                    site=resource["site"],
                    anime=anime["id"],
                ).execute()
                logging.info(f"Inserted resource {resource['id']}")

            for theme in anime["animethemes"]:
                if len(theme["animethemeentries"]) > 0 and len(theme["animethemeentries"][0]["videos"]) > 0:
                    path  = Path(f"./{config.animethemes_output_path}{theme["animethemeentries"][0]["videos"][0]["audio"]["path"]}")
                    filepath = path.as_posix()
                    if(not os.path.exists(filepath)):
                        path.parent.mkdir(parents=True, exist_ok=True)

                        try:
                            urllib.request.urlretrieve(theme["animethemeentries"][0]["videos"][0]["audio"]["link"], filepath)
                        except Exception as e:
                            logging.error(f"Failed to download {theme['animethemeentries'][0]['videos'][0]['audio']['link']} to {filepath}: {e}")
                            continue

                        logging.info(f"Downloaded {theme['animethemeentries'][0]['videos'][0]['audio']['link']} to {filepath}")

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

                    logging.info(f"Inserted animetheme {theme['id']}")

        pagenumber += 1