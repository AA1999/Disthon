from discord.abc.discordobject import DiscordObject
from discord.types.avatar import Avatar


class AbstractUser(DiscordObject):
    __slots__ = ('_id', '_created_at', '_avatar',
                 '_bot', '_username', '_discriminator')

    _avatar: Avatar
    _bot: bool
    _username: str
    _discriminator: str

    @property
    def avatar(self):
        return self._avatar

    @property
    def bot(self):
        return self._bot

    @property
    def username(self):
        return self._username

    @property
    def discriminator(self):
        return self._discriminator

    @property
    def tag(self):
        return f'{self.username}#{self.discriminator}'

    @property
    def mention(self):
        return f'<@!{self._id}>'

    def mentioned_in(self, message: Message):
        if message.mention_everyone:
            return True
        return any(user.id == self.id for user in message.mentions)
