from discord.errors.discordhttpexception import DiscordHTTPException


class DiscordForbidden(DiscordHTTPException):

    def __init__(self, message: str = 'Access forbidden for requested object.'):
        super().__init__(message=message, code=403)
