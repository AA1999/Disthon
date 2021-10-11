from enum import IntEnum


class WebhookType(IntEnum):
    incoming = 1
    channel_follower = 2
    application = 3
