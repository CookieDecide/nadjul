"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import peewee as pw
import os

DB_PATH = "../db/template.db"

# check if db folder exists
if not os.path.exists("../db"):
    os.mkdir("../db")

# link the database file
TEMPLATE_DB = pw.SqliteDatabase(DB_PATH, check_same_thread=False)


class TEMPLATE_TABLE(pw.Model):
    """Template for a database table."""

    primary_key = pw.TextField(primary_key=True)
    text = pw.TextField()
    integer = pw.IntegerField()
    float = pw.FloatField()
    char = pw.CharField()
    bool = pw.BooleanField()
    timestamp = pw.TimestampField()

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
        return self.primary_key

    class Meta:
        database = TEMPLATE_DB
        db_table = "template"


TEMPLATE_DB.connect()
TEMPLATE_DB.create_tables([TEMPLATE_TABLE])
