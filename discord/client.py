from __future__ import annotations

import asyncio
import inspect
from re import L
import sys
import traceback
import typing
from copy import deepcopy

from .api.dataConverters import DataConverter
from .api.httphandler import HTTPHandler
from .api.intents import Intents
from .api.websocket import WebSocket
from .commands.core import Command
from .commands.parser import CommandParser


class Client:

    async def handle_event_error(self, error):
        print(f"Ignoring exception in event {error.event.__name__}", file=sys.stderr)
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr
        )

    async def handle_commands(self, message):
        if message.author.get("bot"):
            return

        command, args, kwargs, extra_kwargs = self.command_parser.parse_message(message)

        if command:
            await command.execute(message, *args, **kwargs, **extra_kwargs)

    def __init__(
        self,
        command_prefix: str,
        *,
        intents: typing.Optional[Intents] = Intents.default(),
        respond_self: typing.Optional[bool] = False,
        case_sensitive: bool=True,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        self._loop: asyncio.AbstractEventLoop = None # create the event loop when we run our client
        self.intents = intents
        self.respond_self = respond_self

        self.stay_alive = True
        self.httphandler = HTTPHandler()
        self.lock = asyncio.Lock()
        self.closed = False
        self.events = {"message_create": [self.handle_commands], "event_error": [self.handle_event_error]}
        self.once_events = {}

        self.command_prefix = command_prefix
        self.commands: typing.Dict[str, Command] = {}

        self.converter = DataConverter(self)
        self.command_parser = CommandParser(self.command_prefix, self.commands, case_sensitive)

    async def login(self, token: str) -> None:
        self.token = token
        async with self.lock:
            self.info = await self.httphandler.login(token)

    async def connect(self) -> None:
        while not self.closed:
            socket = WebSocket(self, self.token)
            async with self.lock:
                g_url = await self.httphandler.gateway()
                if not isinstance(self.intents, Intents):
                    raise TypeError(
                        f"Intents must be of type Intents, got {self.intents.__class__}"
                    )
                self.ws = await asyncio.wait_for(socket.start(g_url), timeout=30)

            while not self.closed:
                await self.ws.receive_events()

    async def alive_loop(self, token: str) -> None:
        self._loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        await self.login(token)
        try:
            await self.connect()
        finally:
            await self.close()

    async def close(self) -> None:
        self.closed = True
        await self.ws.close()
        await self.httphandler.close()

    def run(self, token: str):
        if not self._loop:
            asyncio.run(self.alive_loop(token))
        else:
            self._loop.run_forever(self.alive_loop(token))


    def on(self, event: str = None, *, overwrite: bool = False):
        def wrapper(func):
            self.add_listener(func, event, overwrite=overwrite, once=False)
            return func

        return wrapper

    def once(self, event: str = None, *, overwrite: bool = False):
        def wrapper(func):
            self.add_listener(func, event, overwrite=overwrite, once=True)
            return func

        return wrapper

    def command(self, name=None, **kwargs):
        def inner(func) -> Command:
            command = Command(func, name, **kwargs)
            self.commands[command.name] = command
            return command

        return inner

    def add_listener(
        self,
        func: typing.Callable,
        event: typing.Optional[str] = None,
        *,
        overwrite: bool = False,
        once: bool = False,
    ) -> None:
        event = event or func.__name__
        if not inspect.iscoroutinefunction(func):
            raise TypeError(
                "The callback is not a valid coroutine function. Did you forget to add async before def?"
            )

        if once: # if it's a once event
            if event in self.once_events and not overwrite:
                self.once_events[event].append(func)
            else:
                self.once_events[event] = [func]
        else: # if it's a regular event
            if event in self.events and not overwrite:
                self.events[event].append(func)
            else:
                self.events[event] = [func]

    async def handle_event(self, msg):
        event: str = msg["t"].lower()

        args = self.converter.convert(event, msg["d"])

        for coro in self.events.get(event, []):
            try:
                task = self._loop.create_task(coro(*args))
                await task
            except Exception as error:
                error.event = coro
                await self.handle_event({"d": error, "t": "event_error"})
        
        for coro in self.once_events.pop(event, []):
            try:
                task = self._loop.create_task(coro(*args))
                await task
            except Exception as error:
                error.event = coro
                await self.handle_event({"d": error, "t": "event_error"})

    def get_guild(self, id: int):
        return self.ws.guild_cache.get(id)

    def get_user(self, id: int):
        return self.ws.user_cache.get(id)
