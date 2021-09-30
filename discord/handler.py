import typing
import aiohttp


class Handler:
    def __init__(self):
        self.base_url: str = 'https://discord.com/api/v9/'
        self.user_agent: str = "Disthon test library V0.0.1b"

    async def request(self, method: str, dest: str, *, headers: typing.Optional[dict] = None, data: typing.Optional[dict] = None) -> typing.Union[str, dict]:
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
        self.__session = aiohttp.ClientSession(headers={"Authorization": "Bot " + self.token})
        self.token = token

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

    async def send_message(self, channel_id: int, content: typing.Optional[str] = None):
        payload = {
            'content': content,
        }

        data = await self.request("POST", f"/channels/{channel_id}/messages", data=payload)
        try:
            if data['code'] == 50008:
                raise TypeError("Invalid channel")
            elif data['code'] == 10003:
                raise TypeError("Unknown channel")
        except KeyError:
            return data

    async def fetch_channel(self, channel_id: int):
        data = await self.request("GET", f"/channels/{channel_id}")
        return data

    async def edit_guild_text_channel(self, channel_id: int, **options):
        payload = {k: v for k, v in options.items()}
        await self.request("PATCH", f"/channels/{channel_id}", headers={'Content-Type': 'application/json'}, data=payload)

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
