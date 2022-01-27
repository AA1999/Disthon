from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic import BaseModel

from ..types.snowflake import Snowflake

if TYPE_CHECKING:
    from ..client import Client


class DiscordObject(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: Snowflake
    _client: Client

    def __init__(self, client, **payload):
        super().__init__(_client=client, **payload)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id >> 22
