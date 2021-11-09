from discord.activity.presenseassets import PresenceAssets
from discord.types.snowflake import Snowflake
from discord.activity.baseactivity import BaseActivity


class Activity(BaseActivity):
    __slots__ = ('_state', '_details', '_created_at', '_timestamps', '_assets', '_')

    _application_id: Snowflake
    _assets: PresenceAssets
