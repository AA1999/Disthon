from typing import Optional

from ..types.snowflake import Snowflake

from ..asset import Asset
from ..color import Color
from ..types.avatar import Avatar
from ..types.banner import Banner
from ..types.enums.premiumtype import PremiumType
from ..types.enums.userflags import UserFlags

from ..abc.objectmodel import ObjectModel

class UserModel(ObjectModel):
	id: Snowflake
	username: str
	discriminator: str
	# avatar: Optional[Asset]  TODO: Fix 'value is not a valid dict (type=type_error.dict)' error
	bot: Optional[bool] = False
	system: Optional[bool] = False
	banner: Optional[Banner]
	accent_color: Optional[Color]
	premium_type: Optional[PremiumType]
	public_flags: Optional[UserFlags]