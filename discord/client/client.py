import asyncio
import inspect
import typing

from ..api.handler import Handler
from ..api.websocket import WebSocket
from ..intents import Intents


class Client:

    def __init__(self, *, intents: typing.Optional[Intents] = Intents.default(),
                 respond_self: typing.Optional[bool] = False,
                 loop: typing.Optional[asyncio.AbstractEventLoop] = None) -> None:
        self.__loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self.intents = intents
        self.respond_self = respond_self

        self.stay_alive = True
        self.handler = Handler()
        self.lock = asyncio.Lock()
        self.closed = False
        self.events = {}

    async def login(self, token: str) -> None:
        self.token = token
        async with self.lock:
            self.info = await self.handler.login(token)

    async def connect(self) -> None:
        while not self.closed:
            socket = WebSocket(self, self.token)
            async with self.lock:
                g_url = await self.handler.gateway()
                if not isinstance(self.intents, Intents):
                    raise TypeError(
                        f"Intents must be of type Intents, got {self.intents.__class__}")
                self.ws = await asyncio.wait_for(socket.start(g_url), timeout=30)

            while True:
                await self.ws.receive_events()

    async def alive_loop(self, token: str) -> None:
        await self.login(token)
        try:
            await self.connect()
        finally:
            await self.close()

    async def close(self) -> None:
        await self.handler.close()

    def run(self, token: str):

        def stop_loop_on_completion(_):
            self.__loop.stop()

        future = asyncio.ensure_future(
            self.alive_loop(token), loop=self.__loop)
        future.add_done_callback(stop_loop_on_completion)

        self.__loop.run_forever()

        if not future.cancelled():
            return future.result()

    def event(self, event: str = None):
        def wrapper(func):
            self.add_listener(func, event)
            return func
        return wrapper

    def add_listener(self, func: typing.Callable, event: typing.Optional[str] = None) -> None:
        event = event or func.__name__
        if not inspect.iscoroutinefunction(func):
            raise TypeError(
                "The callback is not a valid coroutine function. Did you forget to add async before def?")

        if event in self.events:
            self.events[event].append(func)
        else:
            self.events[event] = [func]

    async def handle_event(self, msg):
        event = "on_" + msg['t'].lower()

        # don't dispatch when there are no listeners
        if event in self.events:
            for coro in self.events[event]:
                await coro(msg)
        else:
            return
