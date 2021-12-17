import asyncio
import inspect
import re
from typing import Optional, Any, Callable, Iterable

from discord.message import Message


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
            raise ValueError(
                "Callback must be coroutine.\nMaybe you forgot to add the 'async' keyword?."
            )

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
        self.signature = inspect.signature(self._callback)
        self.on_error: Optional[Callable[[Any], Any]] = None

    @property
    def callback(self):
        return self._callback

    async def __call__(self, message: Message, *args, **kwargs):
        await self.callback(message, *args, **kwargs)

    def error(self, function):
        if not asyncio.iscoroutinefunction(function):
            raise ValueError(
                "Command error handler must be coroutine.\nMaybe you forgot to add the 'async' keyword?."
            )

        self.on_error = function
        return function
