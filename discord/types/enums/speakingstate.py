from enum import IntEnum


class SpeakingState(IntEnum):
    none = 0
    voice = 1
    soundshare = 2
    priority = 4

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value
