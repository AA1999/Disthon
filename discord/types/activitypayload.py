from __future__ import annotations

from datetime import datetime
from typing import TypedDict, Optional

from discord.activity.rawactivityassets import RawActivityAssets
from discord.types.enums.activitytype import ActivityType
from discord.types.snowflake import Snowflake


class ActivityTimestamps(TypedDict, total=False):
    start: datetime
    end: datetime


class ActivityParty(TypedDict, total=False):
    id: Snowflake
    size: list[int]


class ActivityEmoji(TypedDict, total=False):
    id: Snowflake
    animated: bool
    name: str


class ActivitySecrets(TypedDict, total=False):
    join: str
    spectate: str
    match: str


class ActivityButton:
    label: str
    url: str


class ActivityPayload(TypedDict, total=False):
    url: Optional[str]
    name: str
    type: ActivityType
    created_at: datetime
    state: Optional[str]
    details: Optional[str]
    timestamps: ActivityTimestamps
    assets: RawActivityAssets
    party: ActivityParty
    application_id: Snowflake
    flags: int
    emoji: Optional[ActivityEmoji]
    secrets: ActivitySecrets
    session_id: Optional[str]
    instance: bool
    buttons: list[ActivityButton]



