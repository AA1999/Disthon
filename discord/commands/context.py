from __future__ import annotations

from typing import Optional, Any

from pydantic import BaseModel

from discord.abc.messageable import Messageable

from discord.commands import Command


class Context(BaseModel, Messageable):
    """The context model which will be used in commands"""
    class Config:
        arbitrary_types_allowed = True

    client: Any
    message: Any  # To avoid circular import errors
    command: Optional[Command] = None

    @property
    def _client(self):
        return self.client  # Make an alias for client because Messageable uses it

    @property
    def guild(self):
        """The guild the command was used in"""
        return self.message.guild

    @property
    def channel(self):
        """The channel the command was used in"""
        return self.message.channel

    @property
    def author(self):
        return self.message.author

    def _get_channel(self):
        return self.channel


Context.update_forward_refs()
