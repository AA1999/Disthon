from __future__ import annotations

from enum import IntEnum


class StickerFormatType(IntEnum):
    png = 1
    apng = 2
    lottie = 3

    @property
    def file_extension(self) -> str:
        lookup: dict[StickerFormatType, str] = {
            StickerFormatType.png: "png",
            StickerFormatType.apng: "png",
            StickerFormatType.lottie: "json",
        }
        return lookup[self]
