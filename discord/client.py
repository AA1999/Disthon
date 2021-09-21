from logging import Handler
import handler
import websocket
import aiohttp
import intents as intent
from os import getenv
import typing
import asyncio

class Client:
    def __init__(self, *, intents: typing.Optional[intent.Intents] = None, respond_self: typing.Optional[bool] = False) -> None:
        self.stay_alive = True
        self.handler = handler.Handler()
        self.lock = asyncio.Lock()
        self.closed = False
        if not intents:
            intents = intent.Intents.default()
        self.intents = intents
        self.events = {}

    async def login(self, token: str) -> None:
        async with self.lock:
            self.info = await self.handler.login(token)
        self.token = token

    async def connect(self) -> None:
        while not self.closed:
            socket = websocket.WebSocket(self, self.token)
            async with self.lock:
                g_url = await self.handler.gateway()
                if not isinstance(self.intents, intent.Intents):
                    raise TypeError(f"Intents must be of type Intents, got {self.intents.__class__}")
                self.ws = await asyncio.wait_for(socket.start(g_url), timeout=30)

            while True:
                await self.ws.receive_events()

    async def alive(self, token: str) -> None:
        await self.login(token)
        try:
            await self.connect()
        finally:
            await self.close()

    async def close(self) -> None:
        await self.handler.close()

    def run(self, token: typing.Optional[str] = None) -> asyncio.Future.result:
        if not token:
            try:
                token = getenv("TOKEN")
                if not len(token) > 0:
                    raise ValueError("No token has been passed, or no valid TOKEN entry in a dotenv could be found.")
            except KeyError:
                	raise ValueError("No token has been passed, or no valid TOKEN entry in a dotenv could be found.")
        self.__loop = asyncio.get_event_loop()

        def stop_loop_on_completion(f):
            self.__loop.stop()

        future = asyncio.ensure_future(self.alive(token), loop=self.__loop)
        future.add_done_callback(stop_loop_on_completion)


        self.__loop.run_forever()

        if not future.cancelled():
            return future.result()

    async def handle_event(self, msg):
        event = msg['t']
        try:
            for coro in self.events[event]:
                await coro(msg)
        except KeyError:
            return