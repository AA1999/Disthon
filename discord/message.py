from __future__ import annotations
from pydantic import BaseModel


class Message(BaseModel):
    def __init__(self, client, data):
        self.client = client
        
