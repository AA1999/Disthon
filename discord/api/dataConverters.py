import inspect
import typing

from discord.types.snowflake import Snowflake

from ..guild import Guild
from ..message import Message

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
        members = data["members"]
        guild = Guild(**data)
        self.client.ws.guild_cache[Snowflake(data["id"])] = guild
        
        for member in members:
            self.client.ws.member_cache[Snowflake(member["user"]["id"])] = member
            self.client.ws.user_cache[Snowflake(member["user"]["id"])] = member["user"]

        return [guild]

    def convert_presence_update(self, data):
        return [data]

    def convert_typing_start(self, data):
        return [data]

    def convert_guild_member_update(self, data):
        return [data]

    def convert(self, event, data):
        func: typing.Callable = self.converters.get(event)
        if not func:
            return data
        return func(data)
