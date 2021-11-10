from __future__ import annotations

import colorsys
import random
import re
from typing import Optional, Union
from pydantic import BaseModel

from .exceptions import InvalidColor

__all__ = ("Color", "Colour")


class Color(BaseModel):

    value: int

    def validate_color(self, color: Optional[Union[int, str]] = None) -> bool:
        if color is None:
            return (
                isinstance(self.value, int) and 0 <= self.value < 16 ** 6
            )  # test if color is in valid range
        elif isinstance(color, int):
            return 0 <= color < 16 ** 6  # test if color is in valid range
        elif color.startswith("#"):
            color = color.replace("#", "0x")  # convert # to 0x for regex match

        match = re.search(r"^0x(?:[0-9a-fA-F]{3}){1,2}$", color)
        return bool(match)

    def __init__(self, value: Union[int, str]):
        if self.validate_color(value):
            if type(value) is str:
                super().__init__(value=int(value, 16))
            else:
                super().__init__(value=value)
        else:
            raise ValueError("Color needs to be 16-bit 6-character value.")

    @classmethod
    def _from_rgb(cls, r: int, g: int, b: int):
        return cls((r << 16) + (g << 8) + b)

    @classmethod
    def _from_hsv(cls, h: float, s: float, v: float):
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return cls._from_rgb(*(int(c * 255) for c in rgb))

    @classmethod
    def default(cls):
        return cls(0)

    @classmethod
    def random(cls, seed: Union[int, str, float, bytes, bytearray, None] = None):
        if seed:
            h = random.Random(seed).random()
        else:
            h = random.random()
        return cls._from_hsv(h, 1.0, 1.0)

    @classmethod
    def teal(cls):
        return cls(0x1ABC9C)

    @classmethod
    def dark_teal(cls):
        return cls(0x11806A)

    @classmethod
    def brand_green(cls):
        return cls(0x57F287)

    @classmethod
    def green(cls):
        return cls(0x2ECC71)

    @classmethod
    def dark_green(cls):
        return cls(0x1F8B4C)

    @classmethod
    def blue(cls):
        return cls(0x3498DB)

    @classmethod
    def dark_blue(cls):
        return cls(0x206694)

    @classmethod
    def purple(cls):
        return cls(0x9B59B6)

    @classmethod
    def dark_purple(cls):
        return cls(0x71368A)

    @classmethod
    def magenta(cls):
        return cls(0xE91E63)

    @classmethod
    def dark_magenta(cls):
        return cls(0xAD1457)

    @classmethod
    def gold(cls):
        return cls(0xF1C40F)

    @classmethod
    def dark_gold(cls):
        return cls(0xC27C0E)

    @classmethod
    def orange(cls):
        return cls(0xE67E22)

    @classmethod
    def dark_orange(cls):
        return cls(0xA84300)

    @classmethod
    def brand_red(cls):
        return cls(0xED4245)

    @classmethod
    def red(cls):
        return cls(0xE74C3C)

    @classmethod
    def dark_red(cls):
        return cls(0x992D22)

    @classmethod
    def lighter_grey(cls):
        return cls(0x95A5A6)

    lighter_gray = lighter_grey

    @classmethod
    def dark_grey(cls):
        return cls(0x607D8B)

    dark_gray = dark_grey

    @classmethod
    def light_grey(cls):
        return cls(0x979C9F)

    light_gray = light_grey

    @classmethod
    def darker_grey(cls):
        return cls(0x546E7A)

    darker_gray = darker_grey

    @classmethod
    def og_blurple(cls):
        return cls(0x7289DA)

    @classmethod
    def blurple(cls):
        return cls(0x5865F2)

    @classmethod
    def greyple(cls):
        return cls(0x99AAB5)

    @classmethod
    def dark_theme(cls):
        return cls(0x36393F)

    @classmethod
    def fuchsia(cls):
        return cls(0xEB459E)

    @classmethod
    def yellow(cls):
        return cls(0xFEE75C)

    def _to_byte(self, byte: int) -> int:
        return (self.value >> (8 * byte)) & 0xFF

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Color) and o.value == self.value

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        return f"#{self.value:0>6x}"

    def __repr__(self) -> str:
        return str(self)

    def __int__(self):
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    @property
    def r(self):
        return self._to_byte(2)

    @property
    def g(self):
        return self._to_byte(1)

    @property
    def b(self):
        return self._to_byte(0)

    def to_rgb(self):
        return self.r, self.g, self.b

    @property
    def value(self):
        return self.value


Colour = Color
