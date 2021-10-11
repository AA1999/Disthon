from enum import IntEnum


class DefaultAvatar(IntEnum):
    blurple = 0
    grey = 1
    gray = 1
    green = 2
    orange = 3
    red = 4

    def __str__(self):
        return self.name
