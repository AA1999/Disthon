from __future__ import annotations

from typing import Optional

from ..abc.discordobject import DiscordObject
from ..color import Color
from ..types.banner import Banner
from ..types.enums.premiumtype import PremiumType
from ..types.enums.userflags import UserFlags


class BaseUser(DiscordObject):
    username: str
    discriminator: str
    # avatar: Optional[Asset]  TODO: Fix 'value is not a valid dict (type=type_error.dict)' error
    bot: Optional[bool] = False
    system: Optional[bool] = False
    mfa_enabled: Optional[bool]
    banner: Optional[Banner]
    accent_color: Optional[Color]
    flags: Optional[UserFlags]
    premium_type: Optional[PremiumType]
    public_flags: Optional[UserFlags]

    @property
    def color(self):
        return Color.default()

    colour = color

    @property
    def mention(self):
        return f"<@!{self.id}>"

    def __str__(self):
        return f"{self.username}#{self.discriminator}"
