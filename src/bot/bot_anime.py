"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""

import discord
from discord.ext import commands
from config import logging
import util.embed
import util.anime_gather
import threading
import config
import asyncio
from resource_manager import shared_resources
from util.checks import is_dev
import util.quiz
from model.db_anime import ANIME_TABLE, ANIMERESOURCES_TABLE, ANIMESERIES_TABLE, ANIMETHEMES_TABLE, ANIMEYEARS_TABLE, MALRATING_TABLE
from peewee import fn
import random
import time


class BotAnime(commands.Cog):
    """Collection of all Anime commands and corresponding utility functions.

    Attributes:
        bot: Reference to discord bot.
    """
    def __init__(self, bot):
        """Initializes the instance.

        Args:
            bot: Discord bot.
        """
        self.bot = bot

    @commands.command(name="ayaya", help="Ayayas.")
    async def ayaya(self, ctx: commands.Context):
        """Prints ayayo in the Chat.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received ayaya request from user {ctx.author}")
        await ctx.send("AYAYO!")
        logging.info(f"Finished ayaya request from user {ctx.author}")

    def parse_aoq_args(self, args):
        """Parses the arguments for the Anime Opening Quiz.

        Args:
            args: Arguments for the quiz.

        Returns:
            Tuple: Parsed arguments.
        """
        # Default values
        parsed_args = {
            "y": "2015-2024",        # years: 2000 or 2000-2005; if only one year is given, the range is to the current year; seperated by "-"
            "p": 20,         # Points to win
            "t": "OP",      # Type: OP, ED; list is possible, seperated by ","
            "r": 10,         # Runtime in seconds
            "s": "START",   # Section: START, RANDOM, END
            "h": 0,         # Hints, degree of hints: 0, 1, 2, 3, 4
            "c": config.lobby_max_players,         # Players
            "d": 0          # Difficulty: 0, 1 ,2 ,3
        }

        # Split by spaces to get each "keyword:value" pair
        pairs = args.split(" ")
        for pair in pairs:
            if ":" in pair:
                key, value = pair.split(":", 1)  # Split by the first ":"
                parsed_args[key] = value

        # Check if the years are valid
        if "-" in parsed_args["y"]:
            years = parsed_args["y"].split("-")
            if len(years) != 2:
                raise ValueError("Invalid year range.")
            
            for year in years:
                if not year.isdigit():
                    raise ValueError("Invalid year range.")
                
            years = [int(year) for year in years]
            parsed_args["y"] = (min(years), max(years))
        else:
            parsed_args["y"] = (int(parsed_args["y"]), time.localtime().tm_year)

        # Check if Points are valid
        try:
            parsed_args["p"] = int(parsed_args["p"])
        except ValueError:
            raise ValueError("Invalid points.")

        # Check if Type is valid
        if "," in parsed_args["t"]:
            types = parsed_args["t"].split(",")
            for t in types:
                if t not in ["OP", "ED"]:
                    raise ValueError("Invalid type.")
            parsed_args["t"] = types
        else:
            if parsed_args["t"] not in ["OP", "ED"]:
                raise ValueError("Invalid type.")
            parsed_args["t"] = [parsed_args["t"]]
            
        # Check if Runtime is valid
        try:
            parsed_args["r"] = int(parsed_args["r"])
        except ValueError:
            raise ValueError("Invalid runtime.")
            
        # Check if Section is valid
        if parsed_args["s"] not in ["START", "RANDOM", "END"]:
            raise ValueError("Invalid section.")
        
        # Check if Hints are valid
        try:    
            parsed_args["h"] = int(parsed_args["h"])
        except ValueError:
            raise ValueError("Invalid hints.")
            
        if parsed_args["h"] not in range(5):
            raise ValueError("Invalid hints.")
            
        # Check if Players are valid
        try:
            parsed_args["c"] = int(parsed_args["c"])
        except ValueError:
            raise ValueError("Invalid players.")
            
        if parsed_args["c"] not in range(1, 11):
            raise ValueError("Invalid players.")
        
        # Check if Difficulty is valid
        try:
            parsed_args["d"] = int(parsed_args["d"])
        except ValueError:
            raise ValueError("Invalid difficulty.")
        
        if parsed_args["d"] not in range(4):
            raise ValueError("Invalid difficulty.")

        return parsed_args
    
    def select_anime_themes(self, parsed_args: dict):
        """Selects anime themes based on the parsed arguments.

        Args:
            parsed_args: Parsed arguments for the quiz.

        Returns:
            Tuple: Anime themes and solution index.
        """
        # select count(*) from animethemes inner join anime on anime.id = animethemes.anime_id where animethemes.type = "OP" and anime.year >= 2018 and anime.year <= 2023;
        anime_themes_count = ANIMETHEMES_TABLE.select() \
                                              .join(ANIME_TABLE) \
                                              .where((ANIMETHEMES_TABLE.type << parsed_args["t"]) 
                                                     & (ANIME_TABLE.year >= parsed_args["y"][0]) 
                                                     & (ANIME_TABLE.year <= parsed_args["y"][1])) \
                                              .count()
        
        logging.info(f"Anime Themes Count: {anime_themes_count}")

        # TODO: Check for duplicate animes

        # Select anime themes based on the parsed arguments
        anime_themes = ANIMETHEMES_TABLE.select() \
                                        .join(ANIME_TABLE) \
                                        .join(MALRATING_TABLE) \
                                        .where((ANIMETHEMES_TABLE.type << parsed_args["t"]) 
                                               & (ANIME_TABLE.year >= parsed_args["y"][0]) 
                                               & (ANIME_TABLE.year <= parsed_args["y"][1])) \
                                        .group_by(ANIMETHEMES_TABLE.path) \
                                        .order_by(MALRATING_TABLE.popularity.asc()) \
                                        .limit(max(100 ,(int(anime_themes_count * config.aoq_sample_size[parsed_args["d"]]))))
        
        anime_themes = random.sample(list(anime_themes), 4)

        solution_index = random.randint(0, 3)

        self.print_anime_themes(anime_themes, solution_index)

        return anime_themes, solution_index
    
    def print_anime_themes(self, anime_themes, solution_index):
        """Prints the anime themes.

        Args:
            anime_themes: List of anime themes.
        """
        for i in range(4):
            if i == solution_index:
                logging.info(f"{i+1}: Solution - {anime_themes[i].anime.name}-{anime_themes[i].slug} - {anime_themes[i].song} - {anime_themes[i].artist} - {anime_themes[i].path}")
                print(f"{i+1}: Solution - {anime_themes[i].anime.name}-{anime_themes[i].slug} - {anime_themes[i].song} - {anime_themes[i].artist} - {anime_themes[i].path}")
            else:
                logging.info(f"{i+1}: Wrong    - {anime_themes[i].anime.name}-{anime_themes[i].slug} - {anime_themes[i].song} - {anime_themes[i].artist} - {anime_themes[i].path}")
                print(f"{i+1}: Wrong    - {anime_themes[i].anime.name}-{anime_themes[i].slug} - {anime_themes[i].song} - {anime_themes[i].artist} - {anime_themes[i].path}")
        print("")

    def prepare_hint(self, anime_theme, hint_level):
        """Prepares the hint for the anime themes.

        Args:
            anime_themes: List of anime themes.
            solution_index: Index of the solution.
            hint_level: Level of the hint.

        Returns:
            Tuple: Hint and solution index.
        """
        hint = ""
        
        if hint_level == 1:
            hint = f"\nHint: {anime_theme.anime.year}"
        elif hint_level == 2:
            hint = f"\nHint: {anime_theme.anime.year}-{anime_theme.song}"
        elif hint_level == 3:
            hint = f"\nHint: {anime_theme.anime.year}-{anime_theme.song}-{anime_theme.artist}"
        elif hint_level == 4:
            hint = f"\nHint: {anime_theme.anime.year}-{anime_theme.song}-{anime_theme.artist}-{anime_theme.anime.studio}"
        
        return hint

    # -Parameter: jahre, punkte zum gewinnen, type(op/ed), Laufzeit der Sample, abschnitt der sample, hints, spielerzahl, (LOCK answers)
    @commands.hybrid_command(name="aoq", help=".")
    async def start_aoq(self, ctx: commands.Context, *, args: str = ""):
        """.

        Args:
            ctx: Context of command invocation.
            args: Arguments for the quiz.
        """
        logging.info(f"Received start_quiz request from user {ctx.author}")

        # Acquire all needed resources
        audio_player = await config.resource_manager[ctx.guild.id].reserve(self, shared_resources.AUDIO_PLAYER)
        if audio_player is None:
            await ctx.send(embed=util.embed.create_embed_error("Audio player is already in use."))
            return
        
        lobby = await config.resource_manager[ctx.guild.id].reserve(self, shared_resources.LOBBY)
        if lobby is None:
            await ctx.send(embed=util.embed.create_embed_error("Lobby is already in use."))
            return
        
        lobby.clear()

        # Parse the arguments
        try:
            parsed_args = self.parse_aoq_args(args)
            print(parsed_args)
        except ValueError as e:
            await ctx.send(embed=util.embed.create_embed_error(str(e)))
            await config.resource_manager[ctx.guild.id].free(self, shared_resources.LOBBY)
            await config.resource_manager[ctx.guild.id].free(self, shared_resources.AUDIO_PLAYER)
            return

        lobby.set_max_players(parsed_args["c"])

        # Start the quiz game
        if lobby.play_loop_task is None or lobby.play_loop_task.done():
            lobby.play_loop_task = asyncio.create_task(self.anime_opening_quiz(ctx, lobby, audio_player, parsed_args))
        
        logging.info(f"Finished start_aoq request from user {ctx.author}")

    async def anime_opening_quiz(self, ctx, lobby, audio_player, parsed_args: dict):
        """Anime Opening Quiz game loop.

        Args:
            ctx: Context of command invocation.
            lobby: Lobby to gather players for.
            audio_player: Audio player to play the songs.
        """
        # Gather players for the quiz lobby and check if it is empty
        await util.quiz.gather_players(ctx, lobby, config.aoq_embed_title)

        if lobby.is_empty():
            await self.acquire_lock(ctx)
            await ctx.send(embed=util.embed.create_embed_error("No players joined the quiz."))
            await config.resource_manager[ctx.guild.id].free(self, shared_resources.LOBBY)
            await config.resource_manager[ctx.guild.id].free(self, shared_resources.AUDIO_PLAYER)
            await self.release_lock(ctx)
            return
        
        # Prepare the quiz (waiting messages till start of quiz)
        await audio_player.join(ctx)
        await util.quiz.prepare_quiz(ctx, config.aoq_embed_title)

        while True:
            await ctx.send("Starting new round!")
            # select * from animethemes inner join anime on animethemes.anime_id = anime.id where animethemes.type = "OP" group by animethemes.path order by RANDOM() limit 4;
            anime_themes, solution_index = self.select_anime_themes(parsed_args)

            hint = self.prepare_hint(anime_themes[solution_index], parsed_args["h"])

            # Send the Question
            await ctx.send(embed=util.embed.create_embed_aoq_quiz(config.aoq_embed_title, "Which Anime Opening is this?", anime_themes, hint))

            await asyncio.sleep(1)

            # Play the song
            await audio_player.play_local(ctx, anime_themes[solution_index].path, parsed_args["r"], parsed_args["s"])

            # Check the given answers(each player can send numbers from 1 - 4 in the chat to give his answer, we are going to check the answer history of the lobby)
            player_answer_tasks = []
            for player_id in lobby.get_players():
                player_answer_tasks.append(asyncio.create_task(self.player_answer_task(ctx, player_id, parsed_args["r"])))

            await asyncio.sleep(parsed_args["r"])

            # Wait for all players to answer
            answers = await asyncio.gather(*player_answer_tasks, return_exceptions=True)
            
            correct_answers = []
            for answer in answers:
                if isinstance(answer, discord.Message):
                    print(f"Answer: {answer.content}, Player: {answer.author.id}") 
                    logging.info(f"Answer: {answer.content}, Player: {answer.author.id}")
                    if int(answer.content) == solution_index + 1:
                        correct_answers.append((answer.author.id, answer.created_at))
                        print(f"{answer.author.mention} Correct!")
                        logging.info(f"{answer.author.mention} Correct!")
                    else:
                        print(f"{answer.author.mention} Wrong!")
                        logging.info(f"{answer.author.mention} Wrong!")
                else:
                    await ctx.send(f"Timeout!")

            fastest_player = (None, None)
            for answer in correct_answers:
                if fastest_player[1] is None or answer[1] < fastest_player[1]:
                    fastest_player = answer
                lobby.increment_score(answer[0])
            if fastest_player[0] is not None:
                lobby.increment_score(fastest_player[0])
                logging.info(f"{ctx.guild.get_member(fastest_player[0]).mention} was the fastest player!")

            # Show the Solution
            await ctx.send(embed=util.embed.create_embed_aop_solution(config.aoq_embed_title, "", anime_themes[solution_index]))

            # Show the scoreboard
            await ctx.send(embed=util.embed.create_embed_scoreboard(ctx, config.aoq_embed_title, "", lobby.get_all_scores()))

            # Check if the game is over
            won = False
            for key, value in lobby.get_all_scores().items():
                if value >= parsed_args["p"]:
                    await ctx.send(f"{ctx.guild.get_member(key).mention} won the quiz with {value} points!")
                    won = True

            await asyncio.sleep(5)

            # stop the song
            audio_player.skip(ctx)

            if won:
                break

        await self.stop_aoq(ctx)

    async def player_answer_task(self, ctx, player_id, timeout: int):
        """Task to check the players answer.

        Args:
            ctx: Context of command invocation.
        """
        try:
            msg = await ctx.bot.wait_for("message", check=lambda m: m.content in ["1", "2", "3", "4"] and m.author.id == player_id, timeout=timeout)
        except asyncio.TimeoutError:
            return None
        return msg


    @commands.hybrid_command(name="aoqstop", help=".")
    async def stop_aoq(self, ctx: commands.Context):
        """.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received stop_quiz request from user {ctx.author}")

        audio_player = await config.resource_manager[ctx.guild.id].check_ownership(self, shared_resources.AUDIO_PLAYER)
        if audio_player is None:
            await ctx.send(embed=util.embed.create_embed_error("Anime is not the owner of the audio player."))
            return
        
        lobby = await config.resource_manager[ctx.guild.id].check_ownership(self, shared_resources.LOBBY)
        if lobby is None:
            await ctx.send(embed=util.embed.create_embed_error("Lobby is already in use."))
            return
        
        lobby.play_loop_task.cancel()
        lobby.clear()
        await audio_player.leave(ctx)

        await ctx.send("Stopped Quiz!")

        await config.resource_manager[ctx.guild.id].free(self, shared_resources.AUDIO_PLAYER)
        await config.resource_manager[ctx.guild.id].free(self, shared_resources.LOBBY)

        logging.info(f"Finished stop_quiz request from user {ctx.author}")

    @start_aoq.before_invoke
    @stop_aoq.before_invoke
    async def acquire_lock(self, ctx):
        """Aquires the audio player lock.

        Args:
            ctx: Context of command invocation.
        """
        audio_player_lock = config.resource_manager[ctx.guild.id].acquire_lock(shared_resources.AUDIO_PLAYER)
        await audio_player_lock.acquire()
        lobby_lock = config.resource_manager[ctx.guild.id].acquire_lock(shared_resources.LOBBY)
        await lobby_lock.acquire()

    @start_aoq.after_invoke
    @stop_aoq.after_invoke
    async def release_lock(self, ctx):
        """Releases the audio player lock.

        Args:
            ctx: Context of command invocation.
        """
        lobby_lock = config.resource_manager[ctx.guild.id].acquire_lock(shared_resources.LOBBY)
        lobby_lock.release()
        audio_player_lock = config.resource_manager[ctx.guild.id].acquire_lock(shared_resources.AUDIO_PLAYER)
        audio_player_lock.release()



    @commands.check(is_dev)
    @commands.command(name="uat", help="Updates the AnimeThemes.", hidden=True)
    async def update_anime_themes(self, ctx: commands.Context):
        """Starts the Thread to update the Database of AnimeThemes.

        Args:
            ctx: Context of command invocation.
        """
        logging.info(f"Received uat request from user {ctx.author}")
        animeGathering = threading.Thread(target=util.anime_gather.gather_years)
        animeGathering.daemon = True
        animeGathering.start()
        logging.info(f"Finished uat request from user {ctx.author}")
