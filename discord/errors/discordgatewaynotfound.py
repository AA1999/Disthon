from discord.errors.discordnotfound import DiscordNotFound


class DiscordGatewayNotFound(DiscordNotFound):

    def __init__(self, message: str = 'Requested gateway not found.'):
        super().__init__(message=message)

