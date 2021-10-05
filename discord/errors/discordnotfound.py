from discord.errors.discordhttpexception import DiscordHTTPException


class DiscordNotFound(DiscordHTTPException):

    def __init__(self, message: str = 'Requested object not found.'):
        super().__init__(message=message, code=404)
