from __future__ import annotations

from os.path import splitext
from typing import Optional

from ..exceptions import DiscordInvalidArgument
from ..cache import LFUCache
from yarl import URL

from enums.validavatarformat import ValidAvatarFormat, ValidStaticAvatarFormat
from image import Image


class Avatar(Image):
    cache: LFUCache
    key: str

    def __init__(self, cache: LFUCache, url: str, key: str):
        self.cache = cache
        self._key = key
        super().__init__(url)

    @classmethod
    def _from_default_avatar(cls, cache: LFUCache, index: int):
        return cls(
            cache,
            url=f'{cls.CDN}/embed/avatars/{index}.png',
            key=str(index)
        )

    @classmethod
    def _from_avatar(cls, cache: LFUCache, user_id: int, avatar: str):
        avatar_format = '.gif' if cls.animated else '.png'
        return cls(
            cache,
            url=f'{cls.CDN}/avatars/{user_id}/{avatar}.{avatar_format}?size=1024',
            key=avatar,
        )

    @classmethod
    def _from_guild_avatar(cls, cache: LFUCache, guild_id: int, member_id: int, avatar: str):
        format = 'gif' if cls.animated else 'png'
        return cls(
            cache,
            url=f"{cls.CDN}/guilds/{guild_id}/users/{member_id}/avatars/{avatar}.{format}?size=1024",
            key=avatar,
        )

    @classmethod
    def _from_icon(cls, cache: LFUCache, object_id: int, icon_hash: str, path: str):
        return cls(
            cache,
            url=f'{cls.CDN}/{path}-icons/{object_id}/{icon_hash}.png?size=1024',
            key=icon_hash,
        )

    @classmethod
    def _from_cover_image(cls, cache: LFUCache, object_id: int, cover_image_hash: str):
        return cls(
            cache,
            url=f'{cls.CDN}/app-assets/{object_id}/store/{cover_image_hash}.png?size=1024',
            key=cover_image_hash,
        )

    @classmethod
    def _from_guild_image(cls, cache: LFUCache, guild_id: int, image: str, path: str):
        return cls(
            cache,
            url=f'{cls.CDN}/{path}/{guild_id}/{image}.png?size=1024',
            key=image,
        )

    @classmethod
    def _from_guild_icon(cls, cache: LFUCache, guild_id: int, icon_hash: str):
        format = 'gif' if cls.animated else 'png'
        return cls(
            cache,
            url=f'{cls.CDN}/icons/{guild_id}/{icon_hash}.{format}?size=1024',
            key=icon_hash,
        )

    @classmethod
    def _from_sticker_banner(cls, cache: LFUCache, banner: int):
        return cls(
            cache,
            url=f'{cls.CDN}/app-assets/710982414301790216/store/{banner}.png',
            key=str(banner),
        )

    @classmethod
    def _from_user_banner(cls, cache: LFUCache, user_id: int, banner_hash: str):
        format = 'gif' if cls.animated else 'png'
        return cls(
            cache,
            url=f'{cls.CDN}/banners/{user_id}/{banner_hash}.{format}?size=512',
            key=banner_hash,
        )

    def __str__(self):
        return self.url

    def __len__(self):
        return len(self.url)

    def __repr__(self):
        return self.url.replace(self.CDN, '')

    def __eq__(self, other):
        return isinstance(other, Avatar) and self.url == other.url

    def __hash__(self):
        return hash(self.url)


    def replace(self, size: Optional[int], format: Optional[ValidAvatarFormat],
                static_format: Optional[ValidAvatarFormat]):
        url = URL(self.url)
        path, _ = splitext(url.path)
        if format is not None:
            if not isinstance(format, ValidAvatarFormat):
                raise DiscordInvalidArgument(f'Format must be in one of the {ValidAvatarFormat.values()}')
            if not isinstance(format, ValidStaticAvatarFormat):
                raise DiscordInvalidArgument(f'Format must be in one of the {ValidStaticAvatarFormat.values()}')
            url = url.with_path(f'{path}.{format}')

    
    @property
    def animated(self):
        return self._is_animated(self.url)
    
    