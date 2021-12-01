from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .types.snowflake import Snowflake

from pydantic import BaseModel

if TYPE_CHECKING:
    from .client import Client
    from .channels.guildchannel import TextChannel


class Message(BaseModel):
    id: Snowflake
    channel_id: int
    content: str

    _client: Client

    def __init__(self, client: Client, data: dict) -> None:
        super().__init__(_client=client, id=Snowflake(data.pop("id")), **data)

    def __str__(self) -> str:
        return self.content

    def __repr__(self) -> str:
        return f"<Message id={self.id} Channel id={self.channel_id} Content={self.content}>"

    @property
    def channel(self) -> Optional[TextChannel]:
        return self._client.converter._get_channel(self.channel_id)
