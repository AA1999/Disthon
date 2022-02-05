from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..types.snowflake import Snowflake


if TYPE_CHECKING:
    from discord import Client


class DiscordObject(BaseModel):
    id: Snowflake
    _client: Client

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, client, **payload):
        super().__init__(_client=client, **payload)
        object.__setattr__(self, "_client", client)  # For some reason pydantic doesn't set the client attribute
        # So we'll set it manually

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id >> 22
