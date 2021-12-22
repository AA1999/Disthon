import asyncio
import re
from typing import Optional, Any, Callable, Iterable

from discord.message import Message
from .errors import CheckFailure


NOT_ASYNC_FUNCTION_MESSAGE = (
    "{0} must be coroutine.\nMaybe you forgot to add the 'async' keyword?."
)


class Command:
    def __init__(
        self,
        callback: Callable[[Any], Any],
        name: str = None,
        *,
        aliases: Iterable[str] = None,
        regex_command: bool = False,
        regex_match_func=re.match,
        regex_flags=0,
        **kwargs
    ):
        if not asyncio.iscoroutinefunction(callback):
            raise ValueError(NOT_ASYNC_FUNCTION_MESSAGE.format("Command callback"))

        self._callback = callback
        self.name = name or self._callback.__name__
        self.is_regex_command = regex_command
        self.regex_match_func = regex_match_func
        self.regex_flags = regex_flags

        if aliases is None:
            self.aliases = []
        else:
            self.aliases = aliases

        self.checks = []
        self.description = kwargs.get("description") or self._callback.__doc__
        self.on_error: Optional[Callable[[Any], Any]] = None

    @property
    def callback(self):
        return self._callback

    def add_check(self, function: Callable[[Message], bool]):
        self.checks.append(function)

    def error(self, function):
        if not asyncio.iscoroutinefunction(function):
            raise ValueError(NOT_ASYNC_FUNCTION_MESSAGE.format("Command error handler"))

        self.on_error = function
        return function

    async def execute(self, message: Message, *args, **kwargs):
        for check in self.checks:
            if asyncio.iscoroutinefunction(check):
                result = await check(message)
            else:
                result = check(message)

            if result is not True:
                raise CheckFailure(self)

        try:
            await self.callback(message, *args, **kwargs)
        except Exception as error:
            if self.on_error:
                await self.on_error(message, error)
            else:
                raise error

    async def __call__(self, message: Message, *args, **kwargs):
        await self.callback(message, *args, **kwargs)


def check(function: Callable[[Message], bool]):

    def inner(command: Command):
        command.add_check(function)
        return command

    return inner
