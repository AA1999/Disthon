import aiohttp
import typing
import os

from aiohttp.connector import Connection

class Handler:
    def __init__(self):
        self.base_url = 'https://discord.com/api/v8/'
        self.user_agent = "Disthon test library V0.0.1b. User: sebkuip#3632"

    async def request(self, method, dest: str, *, headers: typing.Optional[dict]=None, data:typing.Optional[dict]=None):
        async with self.__session.request(method, self.base_url + dest, headers=headers, data=data) as r:
            text = await r.text()
            try:
                if r.headers['content-type'] == 'application/json':
                    return await r.json()
            except KeyError:
                pass

        return text

    async def login(self, token):
        self.__session = aiohttp.ClientSession()
        self.token = token
        try:
            auth_data = await self.request("GET", "/users/@me", headers={"Authorization": "Bot " + self.token})
            return auth_data
        except Exception as e:
            if e.status == 401:
                raise ConnectionError("The token passed is invalid") from e

    async def socket_connect(self, gateway):
        options = {
            'max_msg_size': 0,
            'timeout': 30.0,
            'autoclose': False,
            'headers': {
                'User-Agent': self.user_agent,
            },
            'compress': 9
        }
        return await self.__session.ws_connect(gateway, **options)
