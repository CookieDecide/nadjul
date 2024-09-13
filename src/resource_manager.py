"""Copyright by CookieDecide, Darkuuu
Licensed under MIT License
"""
from asyncio import Lock
from util.audio_player import AudioPlayer
from util.lobby import Lobby
from enum import Enum
from discord.ext.commands import Cog
from config import logging

class shared_resources(Enum):
    AUDIO_PLAYER = 0
    LOBBY = 1

class ResourceManager:
    __assigned_resources: dict
    __resources_dict: dict
    __lock = Lock()

    def __init__(self):
        self.__resources_dict = {shared_resources.AUDIO_PLAYER: AudioPlayer(Lock()),
                                 shared_resources.LOBBY: Lobby(Lock()),
                                }

        self.__assigned_resources = {}
        for resource in shared_resources:
            self.__assigned_resources[resource] = None

    async def reserve(self, requester: Cog, resource: shared_resources):
        """Reserves a resource for the current thread.

        Returns:
            A resource object.
        """
        async with self.__lock:
            logging.info(f"Received reserve request from {requester} for {resource}.")
            if self.__assigned_resources[resource] is None:
                logging.info(f"{resource} reserved for {requester}.")
                self.__assigned_resources[resource] = requester
                return self.__resources_dict[resource]
            elif self.__assigned_resources[resource] == requester:
                return self.__resources_dict[resource]
            else:
                logging.info(f"{resource} is already in use by {self.__assigned_resources[resource]}.")
                return None
    
    async def free(self, requester: Cog, resource: shared_resources):
        """Frees the resource for the current thread.

        Args:
            requester: The requester of the resource.
        """
        async with self.__lock:
            logging.info(f"Received free request from {requester} for {resource}.")
            if self.__assigned_resources[resource] == requester:
                logging.info(f"{resource} freed for {requester}.")
                self.__assigned_resources[resource] = None
                return True
            else:
                logging.warning(f"{resource} is not reserved by {requester}.")
                return False

    async def check_ownership(self, requester: Cog, resource: shared_resources):
        """Checks if the requester owns the resource.

        Args:
            requester: The requester of the check.

        Returns:
            Reference of resource or None.
        """
        async with self.__lock:
            if self.__assigned_resources[resource] == requester:
                return self.__resources_dict[resource]
            else:
                return None
            
    async def free_resource_self(self, resource):
        """Frees the resource for the current thread.

        Args:
            requester: The requester of the resource.
        """
        async with self.__lock:
            for key, value in self.__resources_dict.items():
                if value == resource:
                    logging.info(f"{key} freed for {resource}.")
                    self.__assigned_resources[key] = None
                    return True
            return False
        
    async def is_owner(self, requester: Cog, resource):
        """Checks if the requester is the owner of the resource.

        Args:
            requester: The requester of the check.

        Returns:
            True if the requester is the owner of the resource.
        """
        async with self.__lock:
            for key, value in self.__resources_dict.items():
                if value == resource:
                    return self.__assigned_resources[key] == requester
        
    def acquire_lock(self, resource: shared_resources):
        """Acquires the lock of the resource.

        Args:
            resource: The resource to lock.

        Returns:
            The lock of the resource
        """
        return self.__resources_dict[resource].lock
            
