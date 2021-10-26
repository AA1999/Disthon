from __future__ import annotations

import colorsys
import random
import re
from typing import Union

from .exceptions import InvalidColor

__all__ = ('Color', 'Colour')


class Color:
    __slots__ = ('_value', )

    _value: int

    @staticmethod
    def _is_16_bit(color: Union[int, str]) -> bool:
        temp = ''
        if isinstance(color, int):
            return 0 <= color < pow(16, 6)
        if color.startswith('0x'):
            temp = color.replace('0x', '#')
        elif color.startswith('#'):
            temp = color
        else:
            raise InvalidColor(color, f'{color} is not a valid 16-bit 6-digit color')
        hex_regex = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
        match = re.search(hex_regex, temp)
        return bool(match)

    def __init__(self, value):
        if self._is_16_bit(value):
            self._value = int(value, 16)
        else:
            raise ValueError('Color needs to be 16-bit 6-character value.')

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
    def random(cls, seed: Union[int, str, float, bytes, bytearray, None]):
        return random if seed is None else random.Random(seed)

    @classmethod
    def teal(cls):
        return cls(0x1abc9c)

    @classmethod
    def dark_teal(cls):
        return cls(0x11806a)

    @classmethod
    def brand_green(cls):
        return cls(0x57F287)

    @classmethod
    def green(cls):
        return cls(0x2ecc71)

    @classmethod
    def dark_green(cls):
        return cls(0x1f8b4c)

    @classmethod
    def blue(cls):
        return cls(0x3498db)

    @classmethod
    def dark_blue(cls):
        return cls(0x206694)

    @classmethod
    def purple(cls):
        return cls(0x9b59b6)

    @classmethod
    def dark_purple(cls):
        return cls(0x71368a)

    @classmethod
    def magenta(cls):
        return cls(0xe91e63)

    @classmethod
    def dark_magenta(cls):
        return cls(0xad1457)

    @classmethod
    def gold(cls):
        return cls(0xf1c40f)

    @classmethod
    def dark_gold(cls):
        return cls(0xc27c0e)

    @classmethod
    def orange(cls):
        return cls(0xe67e22)

    @classmethod
    def dark_orange(cls):
        return cls(0xa84300)

    @classmethod
    def brand_red(cls):
        return cls(0xED4245)

    @classmethod
    def red(cls):
        return cls(0xe74c3c)

    @classmethod
    def dark_red(cls):
        return cls(0x992d22)

    @classmethod
    def lighter_grey(cls):
        return cls(0x95a5a6)

    lighter_gray = lighter_grey

    @classmethod
    def dark_grey(cls):
        return cls(0x607d8b)

    dark_gray = dark_grey

    @classmethod
    def light_grey(cls):
        return cls(0x979c9f)

    light_gray = light_grey

    @classmethod
    def darker_grey(cls):
        return cls(0x546e7a)

    darker_gray = darker_grey

    @classmethod
    def og_blurple(cls):
        return cls(0x7289da)

    @classmethod
    def blurple(cls):
        return cls(0x5865F2)

    @classmethod
    def greyple(cls):
        return cls(0x99aab5)

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
        return (self.value >> (8 * byte)) & 0xff

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Color) and o.value == self.value

    def __ne__(self, o: object) -> bool:
        return not self.__eq__(o)

    def __str__(self) -> str:
        return f'#{self.value:0>6x}'

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
        return self._value


Colour = Color
