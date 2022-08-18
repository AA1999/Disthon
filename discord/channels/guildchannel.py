from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from ..types.snowflake import Snowflake

from ..message import Message
from .basechannel import BaseChannel

if TYPE_CHECKING:
	from ..embeds import Embed
	from ..interactions.components import View


class TextChannel(BaseChannel):
	nsfw: bool
	position: int
	category_id: Snowflake

	def __init__(self, client, model):
		super().__init__(client, model)

		self.nsfw = model.nsfw

		self.position = model.position

		self.category_id = model.category_id


class ThreadChannel(BaseChannel):
	__slots__ = (
		"name",
		"id",
		"guild",
		"nsfw",
		"category_id",
		"position",
		"topic",
		"parent",
	)


class VoiceChannel(BaseChannel):
	__slots__ = (
		"name",
		"id",
		"guild",
		"bitrate",
		"user_limit",
		"category_id",
		"position",
	)
