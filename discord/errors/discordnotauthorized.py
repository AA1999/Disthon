from discord.errors.discordhttpexception import DiscordHTTPException


class DiscordNotAuthorized(DiscordHTTPException):

    def __init__(self, message: str = 'Access to the requested object is not authorized.'):
        super().__init__(message=message, code=401)
