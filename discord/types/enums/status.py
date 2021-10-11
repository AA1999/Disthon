from enum import Enum


class Status(Enum):
    online = 'online'
    offline = 'offline'
    idle = 'idle'
    dnd = 'dnd'
    invisible = 'invisible'

    def __str__(self):
        return self.value
