from ..types.snowflake import Snowflake

from pydantic import BaseModel

class ObjectModel(BaseModel):
	id: Snowflake