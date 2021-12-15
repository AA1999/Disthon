from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from ..types.snowflake import Snowflake


class DiscordObject(BaseModel):

    id: Snowflake

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.id.id >> 22
