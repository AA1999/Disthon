from enum import IntEnum


class NSFWLevel(IntEnum):
    default = 0
    explicit = 1
    safe = 2
    age_restricted = 3
