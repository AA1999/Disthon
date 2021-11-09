from __future__ import annotations

from io import BufferedIOBase
from os import PathLike
from typing import ClassVar, Optional, Union

from enums.imagetype import ImageType
from pydantic import BaseModel

from ..cache import LFUCache
from ..exceptions import DiscordException, DiscordNotFound


class Image(BaseModel):

    url: str
    format: ImageType
    cache: Optional[LFUCache]
    CDN: ClassVar[str] = "https://cdn.discordapp.com"

    @staticmethod
    def _is_animated(url: str):
        ret = False
        image_count = 0

        def skip_color_table(fp, packed_byte):

            has_gct = (packed_byte & 0b10000000) >> 7
            gct_size = packed_byte & 0b00000111

            if has_gct:
                global_color_table = fp.read(3 * pow(2, gct_size + 1))

        def skip_image_data(fp):
            """skips the image data, which is basically just a series of sub blocks
            with the addition of the lzw minimum code to decompress the file data"""
            lzw_minimum_code_size = fp.read(1)
            skip_sub_blocks(fp)

        def skip_sub_blocks(fp):
            """skips over the sub blocks

            the first byte of the sub block tells you how big that sub block is, then
            you read those, then read the next byte, which will tell you how big
            the next sub block is, you keep doing this until you get a sub block
            size of zero"""
            num_sub_blocks = ord(fp.read(1))
            while num_sub_blocks != 0x00:
                fp.read(num_sub_blocks)
                num_sub_blocks = ord(fp.read(1))

        with open(url, "rb") as image:
            header = image.read(6)
            if header == b"GIF89a":  # GIF87a doesn't support animation
                logical_screen_descriptor = image.read(7)
                skip_color_table(image, logical_screen_descriptor[4])

                b = ord(image.read(1))
                while b != 0x3B:  # 3B is always the last byte in the gif
                    if b == 0x21:  # 21 is the extension block byte
                        b = ord(image.read(1))
                        if b == 0xF9:  # graphic control extension
                            block_size = ord(image.read(1))
                            image.read(block_size)
                            b = ord(image.read(1))
                            if b != 0x00:
                                raise ValueError("GCT should end with 0x00")

                        elif b == 0xFF:  # application extension
                            block_size = ord(image.read(1))
                            image.read(block_size)
                            skip_sub_blocks(image)

                        elif b == 0x01:  # plain text extension
                            block_size = ord(image.read(1))
                            image.read(block_size)
                            skip_sub_blocks(image)

                        elif b == 0xFE:  # comment extension
                            skip_sub_blocks(image)

                    elif b == 0x2C:  # Image descriptor
                        # if we've seen more than one image it's animated
                        image_count += 1
                        if image_count > 1:
                            ret = True
                            break

                        # total size is 10 bytes, we already have the first byte so
                        # let's grab the other 9 bytes
                        image_descriptor = image.read(9)
                        skip_color_table(image, image_descriptor[-1])
                        skip_image_data(image)

                    b = ord(image.read(1))

        return ret

    def __init__(self, url: str):
        self._url = url
        if ".jpg" in url.lower() or ".jpeg" in url.lower():
            self.format = ImageType.jpeg
        elif ".png" in url.lower():
            self.format = ImageType.png
        elif ".webp" in url.lower():
            self.format = ImageType.webp
        elif ".gif" in url.lower():
            self.format = ImageType.gif
        elif ".json" in url.lower():
            self.format = ImageType.lottie
        else:
            raise DiscordNotFound

    async def to_bytes(self):
        if self.cache is not None:
            return await self.cache.handler.get_from_cdn(self.url)
        raise DiscordException("No cache provided.")

    async def save(
        self,
        fp: Union[str, bytes, PathLike, BufferedIOBase],
        *,
        seek_begin: bool = True
    ) -> int:
        data = await self.to_bytes()
        if isinstance(fp, BufferedIOBase):
            written = fp.write(data)
            if seek_begin:
                fp.seek(0)
            return written
        else:
            with open(fp, "wb") as f:
                return f.write(data)
