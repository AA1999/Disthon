import datetime
from typing import Any, Union, Dict, Optional

__all__ = "Embed"


class Embed:
    def __init__(
        self,
        *,
        title: str = None,
        description: str = None,
        color: int = 0x000000,
        timestamp: Union[datetime.datetime, str] = None,
        url: str = None,
        type: str = "rich"
    ):
        self.title = str(title) if title else None
        self.description = str(description) if description else None
        self.timestamp = str(timestamp) if timestamp else None
        self.color = color
        self.type = type
        self.url = url
        self.fields = []

    def _to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}

    def add_field(self, *, name, value, inline = True, index: Optional[int] = None):
        field = {"name": name,
                 "value": value,
                 "inline": inline}
        if index:
            self.fields.insert(__index=index, __object=field)
        else:
            self.fields.append(field)
        return self

    def set_author(self, *, name, url = None, icon_url = None):
        self.author = {"name": name}
        if url:
            self.author["url"] = url
        if icon_url:
            self.author["icon_url"] = icon_url
        return self

    def set_footer(self, *, text, icon_url = None):
        self.footer = {
            "text": text
        }
        if icon_url:
            self.footer["icon_url"] = icon_url
        return self

    def set_image(self, *, url, height: int = None, width: int = None):
        self.image = {
            "url": url
        }
        if height:
            self.image["height"] = height
        if width:
            self.image["width"] = width
        return self

    def set_thumbnail(self, *, url, height: int = None, width: int = None):
        self.thumbnail = {
            "url": url
        }
        if height:
            self.image["height"] = height
        if width:
            self.image["width"] = width
        return self

    def __len__(self):
        length = len(self.title) + len(self.description)
        for field in self.fields:
            length += len(field["name"]) + len(field["value"])

        if hasattr(self, "footer"):
            length += len(self.footer["text"])
        if hasattr(self, "author"):
            length += len(self.author["name"])
        if hasattr(self, "timestamp"):
            length += len(self.timestamp) if self.timestamp else 0
        return length

    def from_dict(self, data: Dict[str, Any]):
        self.fields = data.get("fields", None)
        self.color = data.get("color", None)
        self.description = data.get("description", None)
        self.footer = data.get("footer", None)
        self.image = data.get("image", None)
        self.title = data.get("title", None)
        self.timestamp = data.get("timestamp", None)
        self.author = data.get("author", None)
        self.url = data.get("url", None)
        self.thumbnail = data.get("thumbnail", None)
        return self
