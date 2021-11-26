import inspect
import typing

from ..activity.activity import Activity
from ..channels.dmchannel import DMChannel
from ..channels.guildchannel import TextChannel, VoiceChannel
from ..color import Color
from ..embeds import Embed
from ..guild import Guild
from ..interactions.components import Component, View
from ..message import Message
from ..role import Role
from ..user.member import Member
from ..user.user import User


class DataConverter:
    def __init__(self, client):
        self.client = client
        self.converters = {}
        for name, func in inspect.getmembers(self):
            if name.startswith("convert_"):
                self.converters[name[8:]] = func

    def _get_channel(self, id):
        return None  # TODO: get channel from cache

    def convert_event_error(self, data):
        return [data]

    def convert_message_create(self, data):
        return [Message(self.client, data)]

    def convert_ready(self, data):
        return []

    def convert_guild_create(self, data):
        return [data]

    def convert_presence_update(self, data):
        return [data]

    def convert_typing_start(self, data):
        return [data]

    def convert_guild_member_update(self, data):
        return [data]

    def convert(self, event, data):
        func: typing.Callable = self.converters.get(event)
        if not func:
            raise NotImplementedError(f"No converter has been implemented for {event}")
        return func(data)
