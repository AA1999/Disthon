import handler
import websocket
import aiohttp
from os import getenv
import typing
import asyncio

class Client:
    def __init__(self):
        self.stay_alive = True
        self.handler = handler.Handler()
        self.lock = asyncio.Lock()

    async def alive(self):
        while self.stay_alive:
            async def create_websocket():
                socket = websocket.WebSocket(self, self.handler.token)
                gw = await socket.gateway()
                socket.connection = await self.handler.socket_connect(gw)

                return socket
            async with self.lock:
                self.websocket = await asyncio.wait_for(create_websocket(), timeout=30)
                await self.websocket.identify()
            while True:
                await self.websocket.receive_events()

    async def login(self, token):
        async with self.lock:
            self.info = await self.handler.login(token)

    def run(self, token: typing.Optional[str] = None):
        if not token:
            try:
                token = getenv("TOKEN")
                if not len(token) > 0:
                    raise ValueError("No token has been passed, an no valid TOKEN entry in a dotenv could be found.")
            except KeyError:
                	raise ValueError("No token has been passed, an no valid TOKEN entry in a dotenv could be found.")

        self.__loop = asyncio.get_event_loop()
        self.__loop.create_task(self.login(token))
        self.__loop.create_task(self.alive())
        self.__loop.run_forever()

client = Client()
client.run("ODg5NDkzMDg1MDIzNzY0NTAw.YUiC_Q.TjN8RGmrbCtmR5yXIZOpHqm3QLw")