from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client


class Message(BaseModel):
    id: int
    channel_id: int
    content: str

    _client: Client
    
    def __init__(self, client, data):
        super().__init__(_client = client, **data)

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"<Message id={self.id} Channel id ={self.channel_id} Content={self.content}>"

    @property
    def channel(self):
        return self._client.converter._get_channel(self.channel_id)