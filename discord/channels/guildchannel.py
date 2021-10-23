from typing import Optional
from Disthon.discord.types.snowflake import Snowflake
from discord.channels.basechannel import BaseChannel
from discord.guild.guild import GuildChannel
import discord.abc


class TextChannel(discord.abc.GuildChannel):
    __slots__ = (
        "name",
        "id",
        "guild",
        "nsfw",
        "category_id",
        "position"
    )

  
