import traceback


class DiscordException(Exception):
    _message: str
    _code: int

    def __init__(self, message: str):
        _message = message

    def print_traceback(self):
        traceback.print_exception(DiscordException, self, self.__traceback__)

    def __repr__(self):
        return f'Error message: {self._message}'

    def __str__(self):
        return self._message
