"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""
from logging import getLogger

command_prefix = ">"  # prefix to invoke a command in discord message
bot_description = "Discord bot"  # Description of the Discord bot
log_path = "logs/"  # Path of log file. Currently only one log file to be used
animethemes_output_path = "animethemes/"  # Path to store anime themes
youtube_output_path = "YT/"
youtube_file_extension = "mp4"
img_path = "img/"
db_path = "db/"

lobby_max_players = 2
aoq_embed_title = "Anime Opening Quiz"
aoq_sample_size = [0.1 ,0.2, 0.4, 1]

resource_manager = {}
logging = getLogger("application")
