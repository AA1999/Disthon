from enum import IntEnum


class VerificationLevel(IntEnum):
    none = 0
    low = 1
    medium = 2
    high = 3
    highest = 4

    def __str__(self):
        return self.name
