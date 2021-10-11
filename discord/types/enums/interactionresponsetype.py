from enum import IntEnum


class InteractionResponseType(IntEnum):
    pong = 1
    channel_message = 4
    deferred_channel_message = 5
    deferred_message_update = 6
    message_update = 7
