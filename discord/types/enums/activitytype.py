from enum import IntEnum


class ActivityType(IntEnum):
    unknown = -1
    playing = 0
    steaming = 1
    listening = 2
    watching = 3
    custom = 4
    competing = 5

