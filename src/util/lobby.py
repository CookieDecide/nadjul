"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""
import config
import asyncio

class Lobby():
    __players: dict
    __max_players: int
    play_loop_task: asyncio.Task
    lock: asyncio.Lock

    def __init__(self, lock: asyncio.Lock):
        self.lock = lock
        self.play_loop_task = None
        self.__players = {}
        self.__max_players = config.lobby_max_players

    def add_player(self, player: int):
        if len(self.__players) >= self.__max_players:
            return False
        self.__players[player] = 0
        return True

    def remove_player(self, player: int):
        if player in self.__players:
            del self.__players[player]
            return True
        return False
    
    def get_number_of_players(self):
        return len(self.__players)

    def get_players(self):
        return self.__players
    
    def clear(self):
        self.__players = {}

    def is_empty(self):
        return len(self.__players) == 0
    
    def is_full(self):
        return len(self.__players) == self.__max_players
    
    def get_all_scores(self):
        return self.__players
    
    def get_score(self, player: int):
        if player not in self.__players:
            return None
        return self.__players[player]
    
    def set_score(self, player: int, score: int):
        if player not in self.__players:
            return False
        self.__players[player] = score
        return True
    
    def increment_score(self, player: int):
        if player not in self.__players:
            return False
        self.__players[player] += 1
        return True
    
    def decrement_score(self, player: int):
        if player not in self.__players:
            return False
        self.__players[player] -= 1
        return True
    
    def change_score_by(self, player: int, change: int):
        if player not in self.__players:
            return False
        self.__players[player] += change
        return True
    
    def get_ranking(self):
        return dict(sorted(self.__players.items(), key=lambda x: x[1], reverse=True))
    
    def set_max_players(self, max_players: int):
        self.__max_players = max_players