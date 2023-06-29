"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import peewee as pw
import os

DB_PATH = "../db/audio.db"

# check if db folder exists
if not os.path.exists("../db"):
    os.mkdir("../db")

# link the database file
AUDIO_DB = pw.SqliteDatabase(DB_PATH, check_same_thread=False)


class YOUTUBE_TABLE(pw.Model):
    """Template for a database table."""

    url = pw.TextField(primary_key=True, unique=True)
    title = pw.TextField()
    length = pw.IntegerField()
    filepath = pw.TextField()
    filename = pw.TextField()
    thumbnail_url = pw.TextField()
    timestamp = pw.TimestampField()
    hash_ = pw.TextField(unique=True)

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
        return self.title

    class Meta:
        database = AUDIO_DB
        db_table = "audio"


AUDIO_DB.connect()
AUDIO_DB.create_tables([YOUTUBE_TABLE])
