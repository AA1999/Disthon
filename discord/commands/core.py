from __future__ import annotations

import asyncio
import re
from typing import Optional, Any, Callable, Iterable, TYPE_CHECKING

from discord.message import Message
from .errors import CheckFailure

if TYPE_CHECKING:
    from .context import Context


NOT_ASYNC_FUNCTION_MESSAGE = (
    "{0} must be coroutine.\nMaybe you forgot to add the 'async' keyword?."
)


class Command:
    def __init__(
        self,
        callback: Callable[[Any], Any],
        name: str = None,
        *,
        qualified_name: str = None,
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
        self.qualified_name = qualified_name

        if self.qualified_name is None and regex_command is True:
            raise TypeError("You need to supply the qualified_name for regex commands")

        elif self.qualified_name is None and regex_command is False:
            self.qualified_name = name

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

    async def run_checks(self, context):
        for check in self.checks:
            if asyncio.iscoroutinefunction(check):
                result = await check(context)
            else:
                result = check(context)

            if result is not True:
                raise CheckFailure(self)


    async def execute(self, context: Context, *args, **kwargs):
        """Runs the checks and execute the command"""
        await self.run_checks(context)

        try:
            await self.callback(context, *args, **kwargs)
        except Exception as error:
            if self.on_error:
                await self.on_error(context, error)
            else:
                raise error

    async def __call__(self, context: Context, *args, **kwargs):
        """Execute the command when the instance is called
           NOTE: This method does not validate checks"""
        await self.callback(context, *args, **kwargs)


def check(function: Callable[[Message], bool]):

    def inner(command: Command):
        command.add_check(function)
        return command

    return inner
