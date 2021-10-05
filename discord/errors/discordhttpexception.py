from http.client import HTTPException

from discord.errors.discordexception import DiscordException


class DiscordHTTPException(DiscordException, HTTPException):
    _code: int

    def __init__(self, message: str, code: int):
        self._code = code
        super().__init__(message)

    def __str__(self):
        return f'Error {self._code}: {self._message}'

    def __repr__(self):
        return f'Error code: {self._code} Message: {self._message}'

