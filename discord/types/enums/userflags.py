from enum import IntFlag


class UserFlags(IntFlag):
    none = 0
    discord_staff = 1 << 0
    partnered_server_owner = 1 << 1
    hyper_squad_events = 1 << 2
    bug_hunter_level_1 = 1 << 3
    house_bravery = 1 << 6
    house_brilliance = 1 << 7
    house_balance = 1 << 8
    early_supporter = 1 << 9
    team_user = 1 << 10
    bug_hunter_level_2 = 1 << 14
    verified_bot = 1 << 16
    early_verified_bot_developer = 1 << 17
    discord_certified_moderator = 1 << 18
