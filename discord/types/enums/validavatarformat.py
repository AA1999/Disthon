from enum import Enum


class ValidAvatarFormat(Enum):
    png = '.png'
    jpg = '.jpg'
    jpeg = '.jpeg'
    webp = '.webp'
    gif = '.gif'

    @staticmethod
    def values():
        return [ValidAvatarFormat.png.value, ValidAvatarFormat.jpg.value, ValidAvatarFormat.jpeg.value,
                ValidAvatarFormat.webp.value, ValidAvatarFormat.gif.value]


class ValidStaticAvatarFormat(Enum):
    png = '.png'
    jpg = '.jpg'
    jpeg = '.jpeg'
    webp = '.web'

    @staticmethod
    def values():
        return [ValidStaticAvatarFormat.png.value, ValidStaticAvatarFormat.jpg.value,
                ValidStaticAvatarFormat.jpeg.value, ValidStaticAvatarFormat.webp.value]
