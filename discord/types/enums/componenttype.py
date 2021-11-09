from enum import IntEnum


class ComponentType(IntEnum):
    action_row = 1
    button = 2
    select = 3

    def __int__(self):
        return self.value
