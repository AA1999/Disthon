from __future__ import annotations

from typing import Optional

from discord.channels.guildchannel import GuildChannel
from discord.member.member import Member
from discord.role.role import Role
from discord.user.user import User
from pydantic import BaseModel

from .enums.locale import Locale
from .enums.nsfwlevel import NSFWLevel
from .enums.verificationlevel import VerificationLevel
from .snowflake import Snowflake


class UnavailableGuild(BaseModel):
    id: Snowflake
    unavaliable: bool

class BanPayload(BaseModel):
    reason: Optional[str]
    user: User


class GuildPayload(BaseModel):
    icon_hash: Optional[str]
    owner: bool
    permissions: str
    widget_enabled: bool
    widget_channel_id: Optional[Snowflake]
    joined_at: Optional[str]
    large: bool
    member_count: int
    voice_states: list[GuildVoiceState]
    members: list[Member]
    channels: list[GuildChannel]
    presences: list[PartialPresenceUpdate]
    threads: list[Thread]
    max_presences: Optional[int]
    max_members: int
    premium_subscription_count: int
    max_video_channel_users: int
    name: str
    icon: Optional[str]
    splash: Optional[str]
    discovery_splash: Optional[str]
    emojis: list[Emoji]
    features: list[GuildFeature]
    description: Optional[str]
    owner_id: Snowflake
    region: str
    afk_channel_id: Optional[Snowflake]
    afk_timeout: int
    verification_level: VerificationLevel
    default_message_notifications: DefaultMessageNotificationLevel
    explicit_content_filter: ExplicitContentFilterLevel
    roles: list[Role]
    mfa_level: MFALevel
    nsfw_level: NSFWLevel
    application_id: Optional[Snowflake]
    system_channel_id: Optional[Snowflake]
    system_channel_flags: int
    rules_channel_id: Optional[Snowflake]
    vanity_url_code: Optional[str]
    banner: Optional[str]
    premium_tier: PremiumTier
    preferred_locale: Locale
    public_updates_channel_id: Optional[Snowflake]
