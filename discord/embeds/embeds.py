from __future__ import annotations

import re
import traceback
from datetime import datetime
from http.client import InvalidURL
from typing import Any, Final, Mapping, Optional, Type, Union

import arrow
from arrow import Arrow
from ..color.color import Color
from ..errors.exceptions import EmptyField, InvalidColor
from ..types.enums.embedtype import EmbedType
from ..utils.datetime import parse_time, utcnow
from pydantic import BaseModel, validator

__all__ = ('Embed',)

class EmbedFooter(BaseModel):
    text: Optional[str] = None
    icon_url: Optional[str] = None
    
class EmbedField(BaseModel):
    name: str
    value: str
    inline: bool = False

class EmbedMedia(BaseModel):
    url: Optional[str] = None
    proxy_url: Optional[str] = None
    height: Optional[int] = 0
    width: Optional[int] = 0
    
    @validator('url')
    def _validate_url(self, url):
        if url is None:
            return url
        url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        match = re.findall(url_regex, url)
        if len(match) != 1:
            raise InvalidURL
        return url

class EmbedVideo(BaseModel):
    url: Optional[str] = None
    height: Optional[int] = 0
    width: Optional[int] = 0
    
    @validator('url')
    def _validate_url(self, url):
        if url is None:
            return url
        url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        match = re.findall(url_regex, url)
        if len(match) != 1:
            raise InvalidURL
        return url

class EmbedProvider(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    
    @validator('url')
    def _validate_url(self, url):
        if url is None:
            return url
        url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        match = re.findall(url_regex, url)
        if len(match) != 1:
            raise InvalidURL
        return url

class EmbedAuthor(BaseModel):
    name: str
    url: Optional[str] = None
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None
    
    @validator('name')
    def _validate_name(self, name):
        if name is None:
            return name
        if isinstance(name, str):
            if len(name) == 0:
                raise EmptyField
            else:
                return name
        raise ValueError
        
    @validator('url')
    def _validate_url(self, url):
        if url is None:
            return url
        url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        match = re.findall(url_regex, url)
        if len(match) != 1:
            raise InvalidURL
        return url
    
class Embed(BaseModel):
    color: Union[Color, int] = Color(Color.random(972))
    title: Optional[str]
    _type: Final[EmbedType] = EmbedType.rich
    author: Optional[EmbedAuthor]
    url: Optional[str]
    description = Optional[str] 
    timestamp: Optional[Arrow]
    thumbnail: Optional[EmbedMedia] = None
    image: Optional[EmbedMedia] = None
    footer: Optional[EmbedFooter] = None
    fields: list[EmbedField] = []
    video: Optional[EmbedVideo] = None
    provider: Optional[EmbedProvider] = None
    
    
    @validator('url')
    def _validate_url(self, url):
        url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        match = re.findall(url_regex, url)
        if len(match) != 1:
            raise InvalidURL
        return url
        
    @classmethod
    def from_dict(cls: Type[Embed], data: Mapping[str, Any]):
        self: Embed = cls.__new__(cls)
        self.title = data.get('title', None)
        self.color = data.get('color', Color(Color.random(972)))
        self.url = data.get('url', None)
        self.description = data.get('description', None)
        self.author = data.get('author', None)
        try:
            self.timestamp = parse_time(data['timestamp'])
            if not self.timestamp:
                self.timestamp = utcnow()
        except KeyError:
            pass
        self.footer = data.get('footer', None)
        self.fields = data.get('fields', None)
        self.image = data.get('image', None)
        self.thumbnail = data.get('thumbnail', None)
        self.video = data.get('video', None)
        self.provider = data.get('provider', None)
        
    def __len__(self) -> int:
        
        total = 0
        if self.title:
            total += len(self.title)
        if self.description:
            total += len(self.description)
        for field in self.fields:
            total += len(field.name) + len(field.value)
        if self.footer:
            total += len(self.footer.text) if self.footer.text else 0
        if self.author:
            total += len(self.author.name) if self.author.name else 0
        return total
        
            
    def __bool__(self):
        return any((self.color, self.title, self.url, self.description, self.timestamp, self.author, 
                    self.thumbnail, self.video, self.provider))
    
    def set_footer(self, *, text: Optional[str] = None, icon_url: Optional[str] = None) -> Embed:
        if not self.footer:
            self.footer = EmbedFooter(text=text, icon_url=icon_url)
            return self
        self.footer.text = text
        self.footer.icon_url = icon_url
        return self
    
    def remove_footer(self) -> Embed:
        del self.footer
        return self
    
    def set_author(self, *, name: str, url: Optional[str] = None, icon_url: Optional[str] = None):
        if self.author is None:
            self.author = EmbedAuthor(name=name, url=url, icon_url=icon_url)
        else:
            self.author.name = name
            self.author.url = url
            self.author.icon_url = icon_url
    
    def remove_author(self) -> Embed:
        del self.author
        return self
    
    def set_image(self, url: str) -> Embed:
        if self.image is None:
            self.image = EmbedMedia(url=url)
        else:
            self.image.url = url
        return self

    def remove_image(self) -> Embed:
        del self.image
        return self
    
    def set_thumbnail(self, url: str) -> Embed:
        if self.thumbnail is None:
            self.thumbnail = EmbedMedia(url=url)
        else:
            self.thumbnail.url = url
        return self
            
    def remove_thumbnail(self):
        del self.thumbnail
        return self
    
    def add_field(self, name: str, value: str, inline: bool = False) -> Embed:
        self.fields.append(EmbedField(name=name, value=value, inline=inline))
        return self
    
    
    def add_fields(self, fields: list[EmbedField]):
        self.fields.extend(fields)
        return self
    
    def set_field(self, name: str, value: str, inline: bool = False) -> Embed:
        self.fields.clear()
        self.fields.append(EmbedField(name=name, value=value, inline=inline))
        return self
    
    def append_field(self, name: str, value: str, inline: bool = False, position: int = None):
        if position is None:
            position = len(self.fields) - 1
        self.fields.insert(position, EmbedField(name=name, value=value, inline=inline))
        return self
    
    def remove_field(self, index: int) -> Embed:
        try:
            self.fields.remove(self.fields[index])
        except ValueError as e:
            print('Ignoring exception in function remove_filed():')
            traceback.print_exception(ValueError, e)
        return self
    
    def set_fields(self, fields: list[EmbedField]) -> Embed:
        self.fields.clear()
        self.fields.extend(fields)
        return self
    
    def clear_fields(self) -> Embed:
        self.fields.clear()
        return self
    
    def set_description(self, description: Optional[str]) -> Embed:
        self.description = description
        return self
    
    def set_title(self, title: Optional[str]):
        self.title = title
        return self
    
    def set_timestamp(self, timestamp: Union[datetime, Arrow, str, int]) -> Embed:
        self.timestamp = arrow.get(timestamp)
        return self
    
    def set_color(self, color: Union[int, Color, str]) -> Embed:
        if isinstance(color, (int, str)) and not Color._is_16_bit(color):
            raise InvalidColor(color, f'{color} is not a valid color value.')
        if isinstance(color, str):
            color = int(color, 16)
        self.color = color
        return self
    
    def set_url(self, url: str) -> Embed:
        url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        if re.search(url_regex, url):
            self.url = url
            return self
        raise InvalidURL
    
    def json(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "type": "rich",
            "description": self.description,
            "url": self.url,
            "timestamp": self.timestamp.astimezone(self.timestamp.tzinfo) if self.timestamp is not None else None,
            "color": Color(self.color).value,
            "fields": self.fields,
            "thumbnail": self.thumbnail.json() if self.thumbnail is not None else None,
            "image": self.image.json() if self.image is not None else None,
            "author": self.author.json() if self.author is not None else None,
            "footer": self.footer.json() if self.footer is not None else None
        }
        
    def to_dict(self) -> dict[str, Any]:
        return self.json()
    
    
    
    @property
    def hex_color(self) -> str:
        return f'#{Color(self.color).r}{Color(self.color).g}{Color(self.color).b}'
    
    @property
    def created_at(self) -> Arrow:
        if self.timestamp:
            return self.timestamp 
        return utcnow()
