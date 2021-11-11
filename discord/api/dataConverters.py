from ..color import Color
from ..embeds import Embed
from ..guild import Guild
from ..message import Message
from ..role import Role
from ..activity.activity import Activity
from ..channels.dmchannel import DMChannel
from ..channels.guildchannel import TextChannel, VoiceChannel
from ..interactions.components import Component, View
from ..user.member import Member
from ..user.user import User

import inspect
import typing

class DataConverter:
    def __init__(self, client):
        self.client = client
        self.converters = {}
        for name, func in inspect.getmembers(self):
            if name.startswith('convert_'):
                self.converters[name[8:]] = func

    def convert_message(self, data):
        return Message(self.client, data)
    
    def convert_ready(self, data):
        return None
    
    def convert_guild_create(self, data):
        return data

    def convert(self, data):
        func: typing.Callable = self.converters.get(data['t'].lower())
        if not func:
            raise NotImplementedError(f"No converter has been implemented for {data['t']}")
        return func(data)