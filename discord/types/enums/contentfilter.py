from enum import IntEnum


class ContentFilter(IntEnum, comparable=True):
    disabled = 0
    no_role = 1
    all_members = 2

    def __str__(self):
        return self.name
