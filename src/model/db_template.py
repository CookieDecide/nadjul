"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import peewee as pw
import os
from playhouse.sqliteq import SqliteQueueDatabase
import config

DB_PATH = os.path.join(config.db_path, "template.db")

# check if db folder exists
if not os.path.exists(config.db_path):
    os.mkdir(config.db_path)

# link the database file
TEMPLATE_DB = SqliteQueueDatabase(DB_PATH, autostart=False)


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

TEMPLATE_DB.start()
TEMPLATE_DB.connect()
TEMPLATE_DB.create_tables([TEMPLATE_TABLE])
