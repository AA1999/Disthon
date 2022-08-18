from ..abc.objectmodel import ObjectModel
from ..types.snowflake import Snowflake

from pydantic import BaseModel

import typing

class BaseChannelModel(ObjectModel):
	name: str

class TextChannelModel(BaseChannelModel):
	nsfw: typing.Optional[bool]
	position: int
	category_id: typing.Optional[Snowflake]