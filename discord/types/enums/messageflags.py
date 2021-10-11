from enum import IntEnum


class MessageFlags(IntEnum):
    crossposted = 1
    is_crossposted = 2
    supress_embeds = 4
    source_message_deleted = 8
    urgent = 16
    has_thread = 32
    ephermal = 64

    