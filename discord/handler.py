import aiohttp
import typing

class Handler:
    def __init__(self):
        self.base_url: str = 'https://discord.com/api/v8/'
        self.user_agent: str = "Disthon test library V0.0.1b. User: sebkuip#3632"

    async def request(self, method: str, dest: str, *, headers: typing.Optional[dict]=None, data:typing.Optional[dict]=None) -> typing.Union[str, dict]:
        async with self.__session.request(method, self.base_url + dest, headers=headers, data=data) as r:
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
        self.__session = aiohttp.ClientSession()
        self.token = token
        
        try:
            auth_data = await self.request("GET", "/users/@me", headers={"Authorization": "Bot " + self.token})
        except ConnectionError as e:
            raise ConnectionError("The token passed is invalid") from e
        
            
        return auth_data

    async def gateway(self) -> str:
        gw_data = await self.request("GET", "/gateway/bot", headers={"Authorization": "Bot " + self.token})
        url = gw_data['url'] + '?encoding=json&v=9&compress=zlib-stream'
        return url

    async def connect(self, url: str) -> aiohttp.ClientWebSocketResponse:
        payload = {
            'timeout': 30.0,
            'autoclose': False,
            'headers': {
                'User-Agent': self.user_agent,
            },
            'compress': 0,
        }
        return await self.__session.ws_connect(url, **payload)

    async def close(self) -> None:
        await self.__session.close()

    async def send_message(self, channel_id: int, content: typing.Optional[str]=None):
        payload = {
            'content': content,
        }

        data = await self.request("POST", f"/channels/{channel_id}/messages", headers={"Authorization": "Bot " + self.token}, data=payload)
        try:
            if data['code'] == 50008:
                raise TypeError("Invalid channel")
            elif data['code'] == 10003:
                raise TypeError("Unknown channel")
        except KeyError:
            return data
