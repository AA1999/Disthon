from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client


class Message(BaseModel):

    client: Client
    id: int
    channel_id: int
    content: str
    
    def __init__(self, client, data):
        self.client = client
        
