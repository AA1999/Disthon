from __future__ import annotations

from ..types.snowflake import Snowflake
from .baseactivity import BaseActivity
from .presenseassets import PresenceAssets


class Activity(BaseActivity):
    __slots__ = ("_state", "_details", "_created_at", "_timestamps", "_assets", "_")

    _application_id: Snowflake
    _assets: PresenceAssets
