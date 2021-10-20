from typing import ClassVar, Dict

from ..exceptions import InvalidIntent


class Intents:
    
    VALID_INTENTS: ClassVar[Dict[str, int]] = {
        'guilds': 0,
        'members': 1,
        'bans': 2,
        'emojis': 3,
        'integrations': 4,
        'webhooks': 5,
        'invites': 6,
        'voice': 7,
        'presence': 8,
        'message': 9,
        'reaction': 10,
        'typing': 11,
        'dm_message': 12,
        'dm_reaction': 13,
        'dm_typing': 14,
    }

    def __init__(self, **kwargs):
        self.value = 0
        for arg in kwargs:
            arg = arg.lower()
            try:
                self.value = self.value + (1 << self.VALID_INTENTS[arg]) if kwargs[arg] else self.value
            except KeyError:
                raise InvalidIntent(arg, f'Invalid intent {arg}. Please check your spelling.')

    def __setattr__(self, name, value):

        if name not in self.VALID_INTENTS:
            raise InvalidIntent(name, 'Specified value is not in the list of valid intents. Please check your spelling')

        bit = 1 << self.VALID_INTENTS[name]
        if value:
            self.value += bit
        else:
            self.value -= bit

    @classmethod
    def none(cls):
        return cls()

    @classmethod
    def all(cls):
        kwargs = {name: True for name in Intents.VALID_INTENTS}
        return cls(**kwargs)

    @classmethod
    def default(cls):
        kwargs = {name: True for name in Intents.VALID_INTENTS}
        kwargs['members'] = False
        kwargs['presence'] = False
        return cls(**kwargs)

