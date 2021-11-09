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

  
