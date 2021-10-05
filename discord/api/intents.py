class InvalidIntent(BaseException):
    def __init__(self, intent):
        self.intent = intent


class Intents:
    VALID_INTENTS = {
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
                raise InvalidIntent(arg)

    def __setattr__(self, name, value):
        # prevent error when setting attribute from the internals
        if name not in self.VALID_INTENTS:
            return super.__setattr__(self, name, value)

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
        kwargs = {}
        for name in Intents.VALID_INTENTS:
            kwargs[name] = True
        return cls(**kwargs)

    @classmethod
    def default(cls):
        kwargs = {}
        for name in Intents.VALID_INTENTS:
            kwargs[name] = True
        kwargs['members'] = False
        kwargs['presence'] = False
        return cls(**kwargs)
