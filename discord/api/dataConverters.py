import inspect
import typing

from discord.types.snowflake import Snowflake
from ..channels.guildchannel import TextChannel

from ..guild import Guild
from ..message import Message
from ..user.user import User
from ..user.member import Member

if typing.TYPE_CHECKING:
    from ..client import Client


class DataConverter:
    def __init__(self, client: "Client"):
        self.client: "Client" = client
        self.converters = {}
        for name, func in inspect.getmembers(self):
            if name.startswith("convert_"):
                self.converters[name[8:]] = func

    def convert_event_error(self, data):
        return [data]

    def convert_message_create(self, data):
        message = Message(self.client, **data)
        self.client.ws.message_cache[message.id] = message
        return [message]

    def convert_ready(self, data):
        return []

    def convert_guild_create(self, data):
        members = data["members"]
        guild = Guild(self.client, **data)
        self.client.ws.guild_cache[Snowflake(data["id"])] = guild
        
        for member_data in members:
            user_data = member_data["user"]
            member_data.pop("user", None)
            member_data["guild"] = guild
            member_data["guild_avatar"] = member_data.get("avatar")
            member_data.pop("avatar", None)

            self.client.ws.member_cache[Snowflake(user_data["id"])] = Member(self.client, **member_data, **user_data)
            self.client.ws.user_cache[Snowflake(user_data["id"])] = User(self.client, **user_data)

        for channel_data in data["channels"]:
            self.client.ws.channel_cache[Snowflake(channel_data["id"])] = TextChannel(self.client, **channel_data)

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
            return [data]
        return func(data)
