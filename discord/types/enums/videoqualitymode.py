from enum import IntEnum


class VideoQualityMode(IntEnum):
    auto = 1
    full = 2

    def __int__(self):
        return self.value
