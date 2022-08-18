from __future__ import annotations

from ..types.snowflake import Snowflake

from pydantic import validator

import typing

from .objectmodel import ObjectModel

from ..user.usermodel import UserModel

class MessageModel(ObjectModel):
	channel_id: Snowflake
	guild_id: Snowflake
	content: str
	author: UserModel