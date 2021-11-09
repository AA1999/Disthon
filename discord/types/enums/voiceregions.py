from enum import Enum


class VoiceRegions(Enum):
    us_west = 'us-west'
    us_east = 'us-east'
    us_south = 'us-south'
    us_central = 'us-central'
    eu_west = 'eu-west'
    eu_central = 'eu-central'
    singapore = 'singapore'
    london = 'london'
    sydney = 'sydney'
    amsterdam = 'amsterdam'
    frankfurt = 'frankfurt'
    brazil = 'brazil'
    hongkong = 'hongkong'
    russia = 'russia'
    japan = 'japan'
    southafrica = 'southafrica'
    south_korea = 'south-korea'
    india = 'india'
    europe = 'europe'
    dubai = 'dubai'
    vip_us_east = 'vip-us-east'
    vip_us_west = 'vip-us-west'
    vip_amsterdam = 'vip-amsterdam'

    def __str__(self):
        return self.value
