import traceback
from http.client import HTTPException
from typing import Optional, Union

from aiohttp import ClientWebSocketResponse
from .interaction import Interaction


class DiscordException(Exception):
    _message: str
    _code: int

    def __init__(self, message: str):
        self._message = message

    def print_traceback(self):
        traceback.print_exception(DiscordException, self, self.__traceback__)

    def __repr__(self):
        return f'Error message: {self._message}'

    def __str__(self):
        return self._message


class DiscordHTTPException(DiscordException, HTTPException):
    _code: int

    def __init__(self, message: str, code: int):
        self._code = code
        super().__init__(message)

    def __str__(self):
        return f'Error {self._code}: {self._message}'

    def __repr__(self):
        return f'Error code: {self._code} Message: {self._message}'

    @property
    def code(self):
        return self._code


class DiscordClientException(DiscordException):
    def __init__(self, message: str):
        super().__init__(message)


class DiscordConnectionClosed(DiscordClientException):
    _code: Optional[int]
    _shard_id: Optional[int]

    def __init__(self, socket: ClientWebSocketResponse, *, shard_id: Optional[int], code: Optional[int] = None):
        self._code = code or socket.close_code or -1
        self._shard_id = shard_id
        super().__init__(f'Shard {shard_id} closed with code {code}.')

    @property
    def code(self):
        return self._code

    @property
    def shard_id(self):
        return self._shard_id


class DiscordForbidden(DiscordHTTPException):

    def __init__(self,
                 message: str = 'Access forbidden for requested object.'):
        super().__init__(message=message, code=403)


class DiscordNotFound(DiscordHTTPException):

    def __init__(self, message: str = 'Requested object not found.'):
        super().__init__(message=message, code=404)


class DiscordGatewayNotFound(DiscordNotFound):

    def __init__(self, message: str = 'Requested gateway not found.'):
        super().__init__(message=message)


class DiscordInteractionResponded(DiscordClientException):
    _interaction: Interaction

    def __init__(self, interaction: Interaction):
        self._interaction = interaction
        super().__init__('This interaction has already been responded to before.')


class DiscordInvalidArgument(DiscordClientException):

    def __init__(self, message: str):
        super().__init__(message)


class DiscordInvalidData(DiscordClientException):

    def __init__(self, message: str):
        super().__init__(message)


class DiscordNoMoreItems(DiscordException):
    def __init__(self, message: str):
        super().__init__(message)


class DiscordNotAuthorized(DiscordHTTPException):

    def __init__(self, message: str = 'Access to the requested object is not authorized.'):
        super().__init__(message=message, code=401)


class DiscordPrivilegedIntentsRequired(DiscordClientException):
    _shard_id: Optional[int]

    def __init__(self, shard_id: Optional[int]):
        self._shard_id = shard_id
        msg = (
            'Shard %s is requesting privileged intents that have not been explicitly enabled in the '
            'developer portal. It is recommended to go to https://discord.com/developers/applications/ '
            'and explicitly enable the privileged intents within your application\'s page. If this is not '
            'possible, then consider disabling the privileged intents instead.'
        )
        super().__init__(msg % shard_id)

    @property
    def shard_id(self):
        return self._shard_id


class DiscordServerError(DiscordHTTPException):

    def __init__(self, message: str = 'Internal server error.'):
        super().__init__(message=message, code=500)


class InvalidSnowflakeException(Exception): 
    _value: str
    _message: str

    def __init__(self, value: str, message: str):
        self._value = value
        self._message = message

class InvalidIntent(ValueError):
    _message: str
    _value: str
    
    def __init__(self, value: str, message: str):
        self._value = value
        self._message = message
    
    def __str__(self) -> str:
        return f'Error message: {self._message} for {self._value}'
    
    def __repr__(self) -> str:
        return f'Message: {self._message}'
    
class InvalidColor(ValueError):
    _message: str
    _value: Union[int, str]
    
    def __init__(self, value: Union[int, str], message: str) -> None:
        self._value = value
        self._message = message
        super().__init__(message)
        
class EmptyField(ValueError):
    _message: str
    
    def __init__(self, message: str = 'Given field cannot be empty'):
        self._message = message
        super().__init__(message)


class DiscordChannelNotFound(DiscordNotFound):
    
    def __init__(self, message: str = 'Requested channel not found.'):
        super().__init__(message=message)

class DiscordChannelForbidden(DiscordForbidden):
    
    def __init__(self, message: str = 'Access forbidden for requested channel.'):
        super().__init__(message=message)
        
