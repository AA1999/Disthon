from __future__ import annotations

from typing import Optional

from ..types.snowflake import Snowflake

from ..abc.discordobject import DiscordObject
from ..asset import Asset
from ..color import Color
from ..types.avatar import Avatar
from ..types.banner import Banner
from ..types.enums.premiumtype import PremiumType
from ..types.enums.userflags import UserFlags

from pydantic import BaseModel

class BaseUser(DiscordObject):
	username: str
	discriminator: str
	# avatar: Optional[Asset]  TODO: Fix 'value is not a valid dict (type=type_error.dict)' error
	bot: Optional[bool] = False
	system: Optional[bool] = False
	banner: Optional[Banner]
	accent_color: Optional[Color]
	premium_type: Optional[PremiumType]
	public_flags: Optional[UserFlags]

	def __init__(self, client, model):
		super().__init__(client, model)

		self.username = model.username

		self.discriminator = model.discriminator

		self.bot = model.bot

		self.system = model.system

		self.banner = model.banner

		self.accent_color = model.accent_color

		self.premium_type = model.premium_type

		self.public_flags = model.public_flags

	@property
	def color(self):
		return Color.default()

	colour = color

	@property
	def mention(self):
		return f"<@!{self.id}>"

	def __str__(self):
		return f"{self.username}#{self.discriminator}"
	
	def __repr__(self):
		return f"<User id={self.id} username={self.username} discriminator={self.discriminator}>"
