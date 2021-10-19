import aiohttp

import typing
from .embeds import Embed
from discord.interactions.components import View


class Handler:
    def __init__(self):
        self.base_url: str = 'https://discord.com/api/v9/'
        self.user_agent: str = "Disthon test library V0.0.1b"

    async def request(self, method: str, dest: str, *, headers: typing.Optional[dict] = None,
                      data: typing.Optional[dict] = None) -> typing.Union[str, dict]:
        async with self.__session.request(method, self.base_url + dest, headers=headers, json=data) as r:
            if not 200 <= r.status < 300:
                if r.status == 401:
                    raise ConnectionError("Not authorized")
            text = await r.text()
            try:
                if r.headers['content-type'] == 'application/json':
                    return await r.json()
            except KeyError:
                pass

            return text

    async def login(self, token: str) -> dict:
        self.token = token
        self.__session = aiohttp.ClientSession(headers={"Authorization": "Bot " + self.token})

        try:
            auth_data = await self.request("GET", "/users/@me")
        except ConnectionError as e:
            raise ConnectionError("The token passed is invalid") from e

        return auth_data

    async def gateway(self) -> str:
        gw_data = await self.request("GET", "/gateway/bot")
        url = gw_data['url'] + '?encoding=json&v=9&compress=zlib-stream'
        return url

    async def connect(self, url: str) -> aiohttp.ClientWebSocketResponse:
        kwargs = {
            'timeout': 100.0,
            'autoclose': False,
            'headers': {
                'User-Agent': self.user_agent,
            },
            'compress': 0,
        }
        return await self.__session.ws_connect(url, **kwargs)

    async def close(self) -> None:
        await self.__session.close()

    async def send_message(self, channel_id: int, content: typing.Optional[str] = None,
                           embeds: typing.Union[Embed, typing.List[Embed]] = None,
                           views: typing.Union[View, typing.List[View]] = None):
        if isinstance(embeds, Embed):
            embeds = [embeds]
        if isinstance(views, View):
            views = [views]

        payload = {}

        if content:
            payload["content"] = content
        if embeds:
            payload["embeds"] = [embed._to_dict() for embed in embeds]
        if views:
            payload["components"] = [view._to_dict() for view in views]

        data = await self.request("POST", f"channels/{channel_id}/messages", data=payload)
        try:
            if data['code'] == 50008:
                raise TypeError("Invalid channel")
            elif data['code'] == 10003:
                raise TypeError("Unknown channel")
        except KeyError:
            return data

    async def edit_message(self, channel_id: int, message_id: int, *, content: typing.Optional[str] = None,
                           embeds: typing.Union[Embed, typing.List[Embed]] = None,
                           views: typing.Union[View, typing.List[View]] = None):
        if isinstance(embeds, Embed):
            embeds = [embeds]
        if isinstance(views, View):
            views = [views]

        payload = {}

        if content:
            payload["content"] = content
        if embeds:
            payload["embeds"] = [embed._to_dict() for embed in embeds]
        if views:
            payload["components"] = [view._to_dict() for view in views]

        return await self.request("PATCH", f"/channels/{channel_id}/messages/{message_id}", data=payload)

    async def delete_message(self, channel_id: int, message_id: int):
        await self.request("DELETE", f"/channels/{channel_id}/messages/{message_id}")

    async def bulk_delete_messages(self, channel_id: int, message_ids: typing.Iterable[int]):
        await self.request("POST", f"/channels/{channel_id}/messages/bulk-delete", data={"messages": message_ids})

    async def add_reaction(self, channel_id: int, message_id: int, emoji: str):
        await self.request("PUT", f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me")

    async def delete_own_reaction(self, channel_id: int, message_id: int, emoji: str):
        await self.request("DELETE", f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me")

    async def delete_user_reaction(self, channel_id: int, message_id: int, user_id: int, emoji: str):
        await self.request("DELETE", f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}")

    async def fetch_message_reactions(self, channel_id: int, message_id: int, emoji: str, after: int = None,
                                      limit: int = None):
        url = f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
        params = {"after": after, "limit": limit}

        if any(params.values()):
            url += "?"
            for k, v in params.items():
                url += f"{k}={v}&"

        await self.request("GET", url)

    async def delete_all_reactions(self, channel_id: int, message_id: int):
        await self.request("DELETE", f"/channels/{channel_id}/messages/{message_id}/reactions")

    async def delete_all_reactions_for_emoji(self, channel_id: int, message_id: int, emoji: str):
        await self.request("DELETE", f"/channels/{channel_id}/messages/{message_id}/reactions/{emoji}")

    async def delete_channel(self, channel_id: int):
        await self.request("DELETE", f"/channels/{channel_id}")

    async def fetch_channel_history(self, channel_id: int, limit=None, around=None, before=None, after=None):
        url = f"/channels/{channel_id}/messages"
        params = {"limit": limit, "around": around, "before": before, "after": after}

        if any(params.values()):
            url += "?"
            for k, v in params.items():
                if v is not None:
                    url += f"{k}={v}&"

        await self.request("GET", url)

    async def fetch_channel(self, channel_id: int):
        data = await self.request("GET", f"/channels/{channel_id}")
        return data

    async def edit_guild_text_channel(self, channel_id: int, **options: typing.Any):
        payload = {k: v for k, v in options.items()}
        await self.request("PATCH", f"/channels/{channel_id}", headers={'Content-Type': 'application/json'},
                           data=payload)

    async def edit_guild_voice_channel(self, channel_id: int, **options: typing.Any):
        payload = {
            'name': options['name'],
            'position': options['position'],
            'bitrate': options['bitrate'],
            'user_limit': options['user_limit'],
            'permission_overwrites': options['overwrites'],
            'parent_id': options['category'],
            'rtc_region': options['region'],
        }
        await self.request("PATCH", f"/channels/{channel_id}", data=payload)
