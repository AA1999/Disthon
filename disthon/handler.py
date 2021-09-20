import aiohttp
import typing

class Handler:
    def __init__(self):
        self.base_url = 'https://discord.com/api/v8/'

    async def request(self, method, dest: str, *, headers: typing.Optional[dict]=None, data:typing.Optional[dict]=None):
        async with self.__session.request(method, self.base_url + dest, headers=headers, data=data) as r:
            text = await r.text()
            try:
                data = await r.json()
            except KeyError:
                pass
            return text, data

    async def login(self, token):
        self.__session = aiohttp.ClientSession()
        self.token = token
        try:
            auth_data = await self.request("GET", "/users/@me", headers={"Authorization": "Bot " + self.token})
            print(auth_data)
        except Exception as e:
            if e.status == 401:
                raise ConnectionError("The token passed is invalid") from e

