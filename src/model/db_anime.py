"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import peewee as pw
import os
from playhouse.sqliteq import SqliteQueueDatabase

DB_PATH = "../db/anime.db"

# check if db folder exists
if not os.path.exists("../db"):
    os.mkdir("../db")

# link the database file
ANIME_DB = SqliteQueueDatabase(DB_PATH, autostart=False)


class ANIMESERIES_TABLE(pw.Model):
    """Anime Series table schematics."""

    id = pw.IntegerField(primary_key=True, unique=True)
    name = pw.TextField(null=True)
    slug = pw.TextField(null=True)

    """
    Field params:
    null = false - allow null values
    index = false - create an index
    unique = false - create unique index
    default = None - default value of column
    primary_key = false - set as primary key
    constraints = None - one or more constraints
    help_text = None - helptext string
    verbose_name = None - userfriendly name
    """

    def __str__(self):
        return self.slug

    class Meta:
        database = ANIME_DB
        db_table = "animeseries"



class ANIME_TABLE(pw.Model):
    """Anime table schematics."""

    id = pw.IntegerField(primary_key=True, unique=True)
    name = pw.TextField(null=False)
    media_format = pw.TextField(null=True)
    season = pw.TextField(null=True)
    slug = pw.TextField(null=True)
    synopsis = pw.TextField(null=True)
    year = pw.IntegerField(null=True)
    img_url = pw.TextField(null=True)
    studio = pw.TextField(null=True)
    series = pw.ForeignKeyField(ANIMESERIES_TABLE, backref="series", null=True)

    """
    Field params:
    null = false - allow null values
    index = false - create an index
    unique = false - create unique index
    default = None - default value of column
    primary_key = false - set as primary key
    constraints = None - one or more constraints
    help_text = None - helptext string
    verbose_name = None - userfriendly name
    """

    def __str__(self):
        return self.slug

    class Meta:
        database = ANIME_DB
        db_table = "anime"



class ANIMERESOURCES_TABLE(pw.Model):
    """Anime Resources table schematics."""

    id = pw.IntegerField(primary_key=True, unique=True)
    external_id = pw.IntegerField(null=True)
    link = pw.TextField(null=True)
    site = pw.TextField(null=True)
    anime = pw.ForeignKeyField(ANIME_TABLE, backref="anime", null=True)

    """
    Field params:
    null = false - allow null values
    index = false - create an index
    unique = false - create unique index
    default = None - default value of column
    primary_key = false - set as primary key
    constraints = None - one or more constraints
    help_text = None - helptext string
    verbose_name = None - userfriendly name
    """

    def __str__(self):
        return self.link

    class Meta:
        database = ANIME_DB
        db_table = "animeresources"



class ANIMETHEMES_TABLE(pw.Model):
    """Anime Themes table schematics."""

    id = pw.IntegerField(primary_key=True, unique=True)
    sequence = pw.IntegerField(null=True)
    slug = pw.TextField(null=True)
    type = pw.TextField(null=True)
    basename = pw.TextField(null=True)
    filename = pw.TextField(null=True)
    path = pw.TextField(null=True)
    size = pw.IntegerField(null=True)
    link = pw.TextField(null=True)
    song = pw.TextField(null=True)
    artist = pw.TextField(null=True)
    anime = pw.ForeignKeyField(ANIME_TABLE, backref="anime", null=True)

    """
    Field params:
    null = false - allow null values
    index = false - create an index
    unique = false - create unique index
    default = None - default value of column
    primary_key = false - set as primary key
    constraints = None - one or more constraints
    help_text = None - helptext string
    verbose_name = None - userfriendly name
    """

    def __str__(self):
        return self.slug

    class Meta:
        database = ANIME_DB
        db_table = "animethemes"



class ANIMEYEARS_TABLE(pw.Model):
    """Anime Years table schematics."""

    year = pw.IntegerField(primary_key=True, unique=True)

    """
    Field params:
    null = false - allow null values
    index = false - create an index
    unique = false - create unique index
    default = None - default value of column
    primary_key = false - set as primary key
    constraints = None - one or more constraints
    help_text = None - helptext string
    verbose_name = None - userfriendly name
    """

    def __str__(self):
        return self.year

    class Meta:
        database = ANIME_DB
        db_table = "animeyears"

ANIME_DB.start()
ANIME_DB.connect()
ANIME_DB.create_tables([ANIME_TABLE, ANIMERESOURCES_TABLE, ANIMESERIES_TABLE, ANIMETHEMES_TABLE, ANIMEYEARS_TABLE])
ANIME_DB.close()
ANIME_DB.connect()