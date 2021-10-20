from typing import Optional

from ..color import Color
from ..types.image import Image


class Banner(Image):
    __slots__ = ('_url', '_format', '_color')
    _color: Optional[Color]

    def __init__(self, url: str, color: Optional[Color]):
        super().__init__(url)
        self._color = color

    @property
    def color(self):
        return self._color

    @property
    def colour(self):
        return self._color
