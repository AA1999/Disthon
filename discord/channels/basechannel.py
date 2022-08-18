from __future__ import annotations

from ..abc.discordobject import DiscordObject
from ..types.snowflake import Snowflake


class BaseChannel(DiscordObject):
	name: str

	def __init__(self, client, model):
		super().__init__(client, model)
		
		self.name = model.name

	@property
	def mention(self):
		return f"<#{self.id}>"

	@property
	def created_at(self):
		return
