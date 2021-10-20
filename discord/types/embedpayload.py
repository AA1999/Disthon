from __future__ import annotations

from ..color.color import Color
from pydantic import BaseModel

from enums.embedtype import EmbedType


class EmbedFooter(BaseModel):
    icon_url: str
    proxy_icon_url: str
    text: str

class EmbedField(BaseModel):
    inline: bool
    name: str
    value: str

class EmbedThumbnail(BaseModel):
    url: str
    proxy_url: str
    height: int
    width: int

class EmbedVideo(BaseModel):
    url: str
    proxy_url: str
    height: str
    width: str

class EmbedImage(BaseModel):
    url: str
    proxy_url: str
    height: int
    width: int


class EmbedAuthor(BaseModel):
    name: str
    url: str
    icon_url: str
    proxy_icon_url: str

class EmbedProvider(BaseModel):
    name: str
    url: str

class EmbedPayload(BaseModel):
    title: str
    type: EmbedType
    description: str
    url: str
    timestamp: str
    color: Color
    footer: EmbedFooter
    image: EmbedImage
    thumbnail: EmbedThumbnail
    video: EmbedVideo
    provider: EmbedProvider
    author: EmbedAuthor
    fields: list[EmbedField]
