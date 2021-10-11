from enum import IntEnum


class InteractionType(IntEnum):
    ping = 1
    application_command = 2
    component = 3
