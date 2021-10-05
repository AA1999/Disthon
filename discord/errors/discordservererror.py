from discord.errors.discordhttpexception import DiscordHTTPException


class DiscordServerError(DiscordHTTPException):

    def __init__(self, message: str = 'Internal server error.'):
        super().__init__(message=message, code=500)
