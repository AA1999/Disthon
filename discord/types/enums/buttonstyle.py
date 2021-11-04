from enum import IntEnum


class ButtonStyle(IntEnum):
    primary = 1
    secondary = 2
    success = 3
    danger = 4
    link = 5

    def __int__(self):
        return self.value
