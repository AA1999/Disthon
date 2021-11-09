from __future__ import annotations

from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel

from ..activity.rawactivityassets import RawActivityAssets
from .enums.activitytype import ActivityType
from .snowflake import Snowflake


class ActivityTimestamps(BaseModel):
    start: datetime
    end: datetime


class ActivityParty(BaseModel):
    id: Snowflake
    size: list[int]


class ActivityEmoji(BaseModel):
    id: Snowflake
    animated: bool
    name: str


class ActivitySecrets(BaseModel):
    join: str
    spectate: str
    match: str


class ActivityButton(BaseModel):
    label: str
    url: str


class ActivityPayload(BaseModel):
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
