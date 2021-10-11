from discord.activity.presenseassets import PresenceAssets
from discord.types.snowflake import Snowflake
from discord.activity.baseactivity import BaseActivity


class Activity(BaseActivity):
    application_id: Snowflake
    assets: PresenceAssets
