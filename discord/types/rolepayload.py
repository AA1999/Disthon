from __future__ import annotations

from typing import TypedDict

from .snowflake import Snowflake

from ..color import Color


class RoleTagsPayload(TypedDict, total=False):
    bot_id: Snowflake
    integration_id: Snowflake
    premium_subscriber: bool


class RolePayload(TypedDict, total=False):
    id: Snowflake
    name: str
    color: Color
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: RoleTagsPayload
