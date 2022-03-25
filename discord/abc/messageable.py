from __future__ import annotations

import abc
import typing

import discord

if typing.TYPE_CHECKING:
    from discord import Client, Embed
    from discord.interactions import View


class Messageable(abc.ABC):
    id: int
    _client: Client

    def _get_channel(self):
        raise NotImplementedError

    async def send(self,
                   content: typing.Optional[str] = None,
                   *,
                   embeds: typing.Union[Embed, typing.List[Embed]] = None,
                   views: typing.Union[View, typing.List[View]] = None
                   ):
        content = str(content) if content is not None else None

        channel = self._get_channel()
        data = await self._client.httphandler.send_message(channel.id, content=content, embeds=embeds, views=views)

        return discord.message.Message(self._client, **data)
